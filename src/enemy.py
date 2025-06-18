import arcade
import arcade.resources
from pyglet.math import Vec3
from array import array
from arcade.gl import BufferDescription
from pygltflib import GLTF2
import numpy as np
import os
import math
import time

import raycast
import gltf_utils


class Enemy():
    def __init__(self, game, walls, enemy_walls, position=Vec3(0, 0, 0), health=100, rotation=Vec3(0, 0, 0)):
        self.player = game.player  # Accept the player/game object directly
        self.game = game  # Store the game context if needed
        self.is_alive = True
        self.position = position
        self.return_position = position
        self.speed = 0.2
        self.normal_speed = 0.2  # Store normal speed
        self.slow_speed = 0.1   # Slowed speed
        self.slow_until = 0      # Time until which enemy is slowed

        self.health = health
        self.max_health = health

        self.rotation = rotation

        self.attack_damage = 1
        self.attack_range = 3.0
        self.agro = False
        self.attack_cooldown = 2  # Time between attacks in milliseconds
        self.pre_attack_time = 0.2  # Time before attack in seconds
        self.last_attack_time = time.time()  # Time when the last attack occurred
        self.pre_attack_timer = 0.0  # Timer for pre-attack animation
        self.is_attacking = False

        self.radius = 1.0  # Radius for collision detection

        self.walls = []
        for wall in walls:
            wall["id"] = 1  # Assign id = 1 to each wall
            self.walls.append(wall)
        for wall in enemy_walls:
            wall["id"] = 1
            self.walls.append(wall)

        self.proximity_radius = 40.0  # Distance within which the enemy will detect the player

    def move(self, player_position, all_enemies):
        # Restore speed if slow duration is over
        if time.time() > self.slow_until and self.speed != self.normal_speed:
            self.speed = self.normal_speed

        distance_to_player = math.sqrt(
            (self.position.x - player_position.x) ** 2 +
            (self.position.y - player_position.y) ** 2 +
            (self.position.z - player_position.z) ** 2
        )

        if (distance_to_player < self.proximity_radius or self.agro) and distance_to_player > 3.0 and self.is_player_in_sight(player_position):
            # Move toward player
            forward = Vec3(
                math.sin(self.rotation.y), 0, math.cos(self.rotation.y)).scale(self.speed)
            new_position = self.position + forward

            # Push past other enemies (apply repulsion instead of blocking)
            push_vec = Vec3(0, 0, 0)
            for other in all_enemies:
                if other["object"] is self or other["object"].is_dead():
                    continue
                offset = new_position - other["object"].position
                distance = offset.mag
                min_dist = self.radius * 2
                if distance < min_dist and distance > 0.01:
                    # Apply a repulsion force
                    push_vec += offset.normalize().scale((min_dist - distance) / min_dist * 0.5)
            # Combine forward and push
            move_vec = forward + push_vec
            if move_vec.mag > 0.01:
                move_vec = move_vec.normalize().scale(self.speed)
                old_position = self.position
                self.position = self.position + move_vec
                if not self.is_position_clear(self.position, self.walls, radius=self.radius):
                    self.position = old_position
            self.is_attacking = False
            self.pre_attack_timer = 0.0
        elif distance_to_player <= 3.0 and self.is_player_in_sight(player_position):
            if not self.is_attacking and (time.time() - self.last_attack_time > self.attack_cooldown):
                # Start pre-attack timer
                print("Preparing to attack player")
                self.is_attacking = True
                self.pre_attack_timer = time.time()
            elif self.is_attacking:
                # Check if pre-attack time has passed
                if time.time() - self.pre_attack_timer >= self.pre_attack_time:
                    self.attack_player(player_position)
                    self.is_attacking = False
        else:
            # Return to original position
            if self.position != self.return_position and self.return_is_in_sight():
                direction_to_return = Vec3(
                    self.return_position.x - self.position.x,
                    self.return_position.y - self.position.y,
                    self.return_position.z - self.position.z
                ).normalize()
                old_position = self.position
                self.position = self.position + \
                    direction_to_return.scale(self.speed)
                if not self.is_position_clear(self.position, self.walls, radius=self.radius):
                    self.position = old_position
            self.is_attacking = False
            self.pre_attack_timer = 0.0
            self.agro = False

    def is_player_in_sight(self, player_position):
        # Check if raycast from enemy to player intersects with any walls
        ray_start = Vec3(self.position.x, self.position.y + 1, self.position.z)
        ray_end = player_position
        ray_direction = Vec3(
            ray_end.x - ray_start.x,
            ray_end.y - ray_start.y,
            ray_end.z - ray_start.z
        ).normalize()
        distance_to_player = math.sqrt(
            (self.position.x - player_position.x) ** 2 +
            (self.position.y - player_position.y) ** 2 +
            (self.position.z - player_position.z) ** 2
        )

        result, _ = raycast.raycast(
            ray_start, ray_direction, self.walls, ray_length=distance_to_player)

        return not result

    def return_is_in_sight(self):
        # raytrace from enemy to return position
        ray_start = Vec3(self.position.x, self.position.y + 1, self.position.z)
        ray_end = self.return_position
        ray_direction = Vec3(
            ray_end.x - ray_start.x,
            ray_end.y - ray_start.y,
            ray_end.z - ray_start.z
        ).normalize()
        distance_to_return = math.sqrt(
            (self.position.x - self.return_position.x) ** 2 +
            (self.position.y - self.return_position.y) ** 2 +
            (self.position.z - self.return_position.z) ** 2
        )
        result, _ = raycast.raycast(
            ray_start, ray_direction, self.walls, ray_length=distance_to_return)
        return not result

    def attack_player(self, player_position):
        # Implement your attack logic here
        print("Attacking player at:", player_position)

        # find the player class and apply damage
        if hasattr(self.player, 'apply_damage'):
            self.player.apply_damage(self.attack_damage)

        self.last_attack_time = time.time()

    def get_world_position(self):
        return self.position

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_rotation(self):
        return self.rotation

    def apply_damage(self, damage):
        self.agro = True
        self.health -= damage
        # Slow the enemy for 1 second when damaged
        self.speed = self.slow_speed
        self.slow_until = time.time() + 1.0  # Slow for 1 second
        if self.health <= 0:
            self.die()

    def die(self):
        # give player currency
        self.game.player.add_currency(10)  # Example: give 10 currency
        print("Enemy has died")
        self.is_alive = False

    def is_dead(self):
        return not self.is_alive

    def is_position_clear(self, pos, walls, radius=1.0):
        # Check if pos is at least 'radius' away from all wall vertices
        for wall in walls:
            if "buffer_data" in wall:
                positions = wall["buffer_data"]
                num_vertices = len(positions) // 5
                for i in range(num_vertices):
                    wall_pos = Vec3(positions[i*5], 0, positions[i*5+2])
                    dist = math.sqrt((pos.x - wall_pos.x) **
                                     2 + (pos.z - wall_pos.z) ** 2)
                    if dist < radius:
                        return False
        return True

    def unstick_from_wall(self):
        # Try to nudge out in 8 directions
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            nudge = Vec3(math.cos(rad), 0, math.sin(rad)
                         ).scale(self.radius * 1.2)
            test_pos = self.position + nudge
            if self.is_position_clear(test_pos, self.walls, radius=self.radius):
                self.position = test_pos
                break


class Enemy1(Enemy):
    def __init__(self, game, walls, enemy_walls, position=Vec3(0, 0, 0), health=100, rotation=Vec3(0, 0, 0), returnhome=True):
        super().__init__(game, walls, enemy_walls, position, health, rotation)
        self.returnhome = returnhome

    def move(self, player_position, all_enemies):
        # Restore speed if slow duration is over
        if time.time() > self.slow_until and self.speed != self.normal_speed:
            self.speed = self.normal_speed

        distance_to_player = math.sqrt(
            (self.position.x - player_position.x) ** 2 +
            (self.position.y - player_position.y) ** 2 +
            (self.position.z - player_position.z) ** 2
        )

        if (distance_to_player < self.proximity_radius or self.agro) and distance_to_player > 3.0 and self.is_player_in_sight(player_position):
            # Move toward player
            forward = Vec3(
                math.sin(self.rotation.y), 0, math.cos(self.rotation.y)).scale(self.speed)
            new_position = self.position + forward

            # Push past other enemies (apply repulsion instead of blocking)
            push_vec = Vec3(0, 0, 0)
            for other in all_enemies:
                if other["object"] is self or other["object"].is_dead():
                    continue
                offset = new_position - other["object"].position
                distance = offset.mag
                min_dist = self.radius * 2
                if distance < min_dist and distance > 0.01:
                    # Apply a repulsion force
                    push_vec += offset.normalize().scale((min_dist - distance) / min_dist * 0.5)
            # Combine forward and push
            move_vec = forward + push_vec
            if move_vec.mag > 0.01:
                move_vec = move_vec.normalize().scale(self.speed)
                old_position = self.position
                self.position = self.position + move_vec
                if not self.is_position_clear(self.position, self.walls, radius=self.radius):
                    self.position = old_position
            self.is_attacking = False
            self.pre_attack_timer = 0.0
        elif distance_to_player <= 3.0 and self.is_player_in_sight(player_position):
            if not self.is_attacking and (time.time() - self.last_attack_time > self.attack_cooldown):
                # Start pre-attack timer
                print("Preparing to attack player")
                self.is_attacking = True
                self.pre_attack_timer = time.time()
            elif self.is_attacking:
                # Check if pre-attack time has passed
                if time.time() - self.pre_attack_timer >= self.pre_attack_time:
                    self.attack_player(player_position)
                    self.is_attacking = False
        else:
            # Only return to original position if returnhome is True
            if self.returnhome and self.position != self.return_position and self.return_is_in_sight():
                direction_to_return = Vec3(
                    self.return_position.x - self.position.x,
                    self.return_position.y - self.position.y,
                    self.return_position.z - self.position.z
                ).normalize()
                old_position = self.position
                self.position = self.position + \
                    direction_to_return.scale(self.speed)
                if not self.is_position_clear(self.position, self.walls, radius=self.radius):
                    self.position = old_position
            self.is_attacking = False
            self.pre_attack_timer = 0.0
            self.agro = False

    def is_player_in_sight(self, player_position):
        # Check if raycast from enemy to player intersects with any walls
        ray_start = Vec3(self.position.x, self.position.y + 1, self.position.z)
        ray_end = player_position
        ray_direction = Vec3(
            ray_end.x - ray_start.x,
            ray_end.y - ray_start.y,
            ray_end.z - ray_start.z
        ).normalize()
        distance_to_player = math.sqrt(
            (self.position.x - player_position.x) ** 2 +
            (self.position.y - player_position.y) ** 2 +
            (self.position.z - player_position.z) ** 2
        )

        result, _ = raycast.raycast(
            ray_start, ray_direction, self.walls, ray_length=distance_to_player)

        return not result

    def return_is_in_sight(self):
        # raytrace from enemy to return position
        ray_start = Vec3(self.position.x, self.position.y + 1, self.position.z)
        ray_end = self.return_position
        ray_direction = Vec3(
            ray_end.x - ray_start.x,
            ray_end.y - ray_start.y,
            ray_end.z - ray_start.z
        ).normalize()
        distance_to_return = math.sqrt(
            (self.position.x - self.return_position.x) ** 2 +
            (self.position.y - self.return_position.y) ** 2 +
            (self.position.z - self.return_position.z) ** 2
        )
        result, _ = raycast.raycast(
            ray_start, ray_direction, self.walls, ray_length=distance_to_return)
        return not result

    def attack_player(self, player_position):
        # Implement your attack logic here
        print("Attacking player at:", player_position)

        # find the player class and apply damage
        if hasattr(self.player, 'apply_damage'):
            self.player.apply_damage(self.attack_damage)

        self.last_attack_time = time.time()

    def get_world_position(self):
        return self.position

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_rotation(self):
        return self.rotation

    def apply_damage(self, damage):
        self.agro = True
        self.health -= damage
        # Slow the enemy for 1 second when damaged
        self.speed = self.slow_speed
        self.slow_until = time.time() + 1.0  # Slow for 1 second
        if self.health <= 0:
            self.die()

    def is_dead(self):
        return not self.is_alive


class Enemy2(Enemy):
    def __init__(self, game, walls, enemy_walls, position=Vec3(0, 0, 0), health=100, rotation=Vec3(0, 0, 0), returnhome=True):
        super().__init__(game, walls, enemy_walls, position, health, rotation)
        self.returnhome = returnhome
        self.game = game
        self.health = 60
        self.max_health = 60

        self.return_position = position  # Store original position

        self.speed = 0.1  # Override speed for Enemy2
        self.preferred_distance = 15.0  # Distance to keep from player
        self.projectile_cooldown = 3.0  # Seconds between shots
        self.last_projectile_time = time.time()
        self.proximity_radius = 50.0  # Distance within which the enemy will detect the player

    def move(self, player_position, all_enemies):
        # Calculate distance to player (ignore y for horizontal distance)
        dx = self.position.x - player_position.x
        dz = self.position.z - player_position.z
        distance_to_player = math.sqrt(dx ** 2 + dz ** 2)
        if distance_to_player > self.proximity_radius:
            # Only return to original position if returnhome is True
            if self.returnhome and self.position != self.return_position:
                direction_to_return = Vec3(
                    self.return_position.x - self.position.x,
                    0,
                    self.return_position.z - self.position.z
                )
                if direction_to_return.mag > 0.1:
                    direction_to_return = direction_to_return.normalize()
                    new_position = self.position + \
                        direction_to_return.scale(self.speed)
                    # Raycast from current to new position to check for wall collision
                    ray_dir = (new_position - self.position).normalize()
                    ray_length = (new_position - self.position).mag
                    result, _ = raycast.raycast(
                        self.position, ray_dir, self.walls, ray_length=ray_length)
                    if not result:
                        self.position = new_position
            return  # Do nothing else if player is too far
        # Only move in xz plane
        direction = Vec3(
            player_position.x - self.position.x,
            0,
            player_position.z - self.position.z
        ).normalize()
        move_vec = Vec3(0, 0, 0)
        moving_away = False
        # Repulsion from other Enemy2s
        repulsion = Vec3(0, 0, 0)
        min_dist = 4.0  # Social distance radius
        for other in all_enemies:
            if other["object"] is self or other["object"].is_dead():
                continue
            if not isinstance(other["object"], Enemy2):
                continue
            offset = self.position - other["object"].position
            dist = math.sqrt(offset.x ** 2 + offset.z ** 2)
            if dist < min_dist and dist > 0.01:
                repulsion += offset.normalize().scale((min_dist - dist) / min_dist)
        # Repulsion from walls (keep distance from walls)
        wall_repulsion = Vec3(0, 0, 0)
        wall_buffer = 4.0  # Increased minimum distance to keep from walls
        for wall in self.walls:
            if "buffer_data" in wall:
                positions = wall["buffer_data"]
                num_vertices = len(positions) // 5
                for i in range(num_vertices):
                    wall_pos = Vec3(positions[i*5], 0, positions[i*5+2])
                    offset = self.position - wall_pos
                    dist = math.sqrt(offset.x ** 2 + offset.z ** 2)
                    if dist < wall_buffer and dist > 0.01:
                        repulse_strength = (wall_buffer - dist) / wall_buffer
                        wall_repulsion += offset.normalize().scale(repulse_strength)
        # Preferred distance logic
        if distance_to_player < self.preferred_distance - 1.0:
            move_vec -= direction
            moving_away = True
        elif distance_to_player > self.preferred_distance + 1.0:
            move_vec += direction
        # Combine all movement influences
        total_vec = move_vec + repulsion.scale(2.0) + wall_repulsion.scale(6.0)
        if total_vec.mag > 0.01:
            total_vec = total_vec.normalize().scale(self.speed)
            new_position = Vec3(
                self.position.x + total_vec.x,
                self.position.y,
                self.position.z + total_vec.z
            )
            # Raycast from current to new position to check for wall collision
            ray_dir = (new_position - self.position).normalize()
            ray_length = (new_position - self.position).mag
            result, _ = raycast.raycast(
                self.position, ray_dir, self.walls, ray_length=ray_length)
            if not result:
                # Check if new_position is too close to any wall; if so, do not move
                too_close_to_wall = False
                for wall in self.walls:
                    if "buffer_data" in wall:
                        positions = wall["buffer_data"]
                        num_vertices = len(positions) // 5
                        for i in range(num_vertices):
                            wall_pos = Vec3(
                                positions[i*5], 0, positions[i*5+2])
                            offset = new_position - wall_pos
                            dist = math.sqrt(offset.x ** 2 + offset.z ** 2)
                            if dist < wall_buffer:
                                too_close_to_wall = True
                                break
                        if too_close_to_wall:
                            break
                if not too_close_to_wall:
                    self.position = new_position
        # Only shoot if not moving and has line of sight
        is_moving = total_vec.mag > 0.01
        if (not is_moving and self.is_player_in_sight(player_position)
                and time.time() - self.last_projectile_time > self.projectile_cooldown):
            self.shoot_projectile_at_player(self.game, player_position)
            self.last_projectile_time = time.time()

    def shoot_projectile_at_player(self, game, player_position):
        # Use the actual player world position (camera is at -game.camera_pos)
        player_world_pos = -game.camera_pos  # Vec3
        enemy_world_pos = self.position      # Vec3
        # Calculate direction from enemy to player (xz plane only)
        direction = Vec3(
            player_world_pos.x - enemy_world_pos.x,
            0,
            player_world_pos.z - enemy_world_pos.z
        ).normalize()
        # Set projectile start position (at enemy's position, with slight y offset)
        projectile_pos = Vec3(
            enemy_world_pos.x, enemy_world_pos.y + 2, enemy_world_pos.z)
        # Set projectile velocity (toward player)
        projectile_velocity = direction.scale(0.2)  # Adjust speed as needed
        # Use game context to create projectile
        projectile = {
            "id": 4,
            "model": projectile_pos,
            "velocity": projectile_velocity,
            "program": game.sphere_program,
            "geometry": game.generate_sphere(0.3, 10, 10, position=Vec3(0, 0, 0)),
        }
        game.projectiles.append(projectile)
        game.objects.append(projectile)
        print(f"Enemy2 shoots projectile at {player_world_pos}")

        # Hard stop: if too close to any wall, do not move at all
        wall_buffer = 8.0  # Very large buffer
        for wall in self.walls:
            if "buffer_data" in wall:
                positions = wall["buffer_data"]
                num_vertices = len(positions) // 5
                for i in range(num_vertices):
                    wall_pos = Vec3(positions[i*5], 0, positions[i*5+2])
                    offset = self.position - wall_pos
                    dist = math.sqrt(offset.x ** 2 + offset.z ** 2)
                    if dist < wall_buffer:
                        return  # Too close to a wall, do not move


class Enemy3(Enemy):
    def __init__(self, game, walls, enemy_walls, position=Vec3(0, 0, 0), health=300, rotation=Vec3(0, 0, 0), returnhome=True):
        super().__init__(game, walls, enemy_walls, position, health, rotation)
        self.returnhome = returnhome
        self.speed = 0.02
        self.normal_speed = 0.1  # Store normal speed
        self.slow_speed = 0.1   # Same as normal speed
        self.health = 300  # Increased health
        self.max_health = 300

    def move(self, player_position, all_enemies):
        # Restore speed if slow duration is over
        if time.time() > self.slow_until and self.speed != self.normal_speed:
            self.speed = self.normal_speed

        distance_to_player = math.sqrt(
            (self.position.x - player_position.x) ** 2 +
            (self.position.y - player_position.y) ** 2 +
            (self.position.z - player_position.z) ** 2
        )

        if (distance_to_player < self.proximity_radius or self.agro) and distance_to_player > 3.0 and self.is_player_in_sight(player_position):
            # Move toward player
            forward = Vec3(
                math.sin(self.rotation.y), 0, math.cos(self.rotation.y)).scale(self.speed)
            new_position = self.position + forward

            # Push past other enemies (apply repulsion instead of blocking)
            push_vec = Vec3(0, 0, 0)
            for other in all_enemies:
                if other["object"] is self or other["object"].is_dead():
                    continue
                offset = new_position - other["object"].position
                distance = offset.mag
                min_dist = self.radius * 2
                if distance < min_dist and distance > 0.01:
                    # Apply a repulsion force
                    push_vec += offset.normalize().scale((min_dist - distance) / min_dist * 0.5)
            # Combine forward and push
            move_vec = forward + push_vec
            if move_vec.mag > 0.01:
                move_vec = move_vec.normalize().scale(self.speed)
                old_position = self.position
                self.position = self.position + move_vec
                if not self.is_position_clear(self.position, self.walls, radius=self.radius):
                    self.position = old_position
            self.is_attacking = False
            self.pre_attack_timer = 0.0
        elif distance_to_player <= 3.0 and self.is_player_in_sight(player_position):
            if not self.is_attacking and (time.time() - self.last_attack_time > self.attack_cooldown):
                # Start pre-attack timer
                self.is_attacking = True
                self.pre_attack_timer = time.time()
            elif self.is_attacking:
                # Check if pre-attack time has passed
                if time.time() - self.pre_attack_timer >= self.pre_attack_time:
                    self.attack_player(player_position)
                    self.is_attacking = False
        else:
            # Only return to original position if returnhome is True
            if self.returnhome and self.position != self.return_position and self.return_is_in_sight():
                direction_to_return = Vec3(
                    self.return_position.x - self.position.x,
                    self.return_position.y - self.position.y,
                    self.return_position.z - self.position.z
                ).normalize()
                old_position = self.position
                self.position += direction_to_return.scale(self.speed)
                if not self.is_position_clear(self.position, self.walls, radius=self.radius):
                    self.position = old_position
            else:
                self.is_attacking = False
                self.pre_attack_timer = 0.0
                self.agro = False

    def is_player_in_sight(self, player_position):
        # Check if raycast from enemy to player intersects with any walls
        ray_start = Vec3(self.position.x, self.position.y + 1, self.position.z)
        ray_end = player_position
        ray_direction = Vec3(
            ray_end.x - ray_start.x,
            ray_end.y - ray_start.y,
            ray_end.z - ray_start.z
        ).normalize()
        distance_to_player = math.sqrt(
            (self.position.x - player_position.x) ** 2 +
            (self.position.y - player_position.y) ** 2 +
            (self.position.z - player_position.z) ** 2
        )

        result, _ = raycast.raycast(
            ray_start, ray_direction, self.walls, ray_length=distance_to_player)

        return not result

    def return_is_in_sight(self):
        # raytrace from enemy to return position
        ray_start = Vec3(self.position.x, self.position.y + 1, self.position.z)
        ray_end = self.return_position
        ray_direction = Vec3(
            ray_end.x - ray_start.x,
            ray_end.y - ray_start.y,
            ray_end.z - ray_start.z
        ).normalize()
        distance_to_return = math.sqrt(
            (self.position.x - self.return_position.x) ** 2 +
            (self.position.y - self.return_position.y) ** 2 +
            (self.position.z - self.return_position.z) ** 2
        )
        result, _ = raycast.raycast(
            ray_start, ray_direction, self.walls, ray_length=distance_to_return)
        return not result

    def attack_player(self, player_position):
        # Implement your attack logic here
        print("Attacking player at:", player_position)

        # find the player class and apply damage
        if hasattr(self.player, 'apply_damage'):
            self.player.apply_damage(self.attack_damage)

        self.last_attack_time = time.time()

    def get_world_position(self):
        return self.position

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_rotation(self):
        return self.rotation

    def apply_damage(self, damage):
        self.agro = True
        self.health -= damage
        # Slow the enemy for 1 second when damaged
        self.speed = self.slow_speed
        self.slow_until = time.time() + 1.0  # Slow for 1 second
        if self.health <= 0:
            self.die()

    def is_dead(self):
        return not self.is_alive


class Miniboss(Enemy):
    def __init__(self, game, walls, enemy_walls, position=Vec3(0, 0, 0), health=500, rotation=Vec3(0, 0, 0)):
        super().__init__(game, walls, enemy_walls, position, health, rotation)
        self.form = 1  # 1 = sword, 2 = gun
        self.geometry_form1 = None  # Sword form geometry
        self.geometry_form2 = None  # Gun form geometry
        # seconds between form switches (now 10s)
        self.form_switch_cooldown = 3.0
        self.last_form_switch = time.time()
        self.health = 1200
        self.max_health = 1200
        # Sword form: melee
        self.sword_attack_range = 5.0
        self.sword_attack_damage = 20
        self.sword_speed = 0.4
        self.sword_dash_speed = 1.0
        self.sword_dash_cooldown = 2.0
        self.sword_dash_duration = 0.2
        self.sword_dash_windup = 0.3
        self.sword_dash_windup_first = 0.35  # First dash windup
        self.sword_dash_windup_repeat = 0.7  # Subsequent dash windup (slower)
        self.sword_last_dash = 0
        self.sword_dashing = False
        self.sword_dash_end_time = 0
        self.sword_dash_direction = None
        self.sword_dash_windup_start = 0
        self.sword_dash_in_windup = False
        self.sword_dash_count = 0  # Track consecutive dashes
        # Gun form: ranged
        self.gun_attack_range = 30.0
        self.gun_attack_damage = 1  # Increased damage
        self.gun_speed = 0.2  # Slower than sword form
        self.gun_projectile_cooldown = 0.45  # Shoots more frequently
        self.gun_burst_count = 3  # Shoots a burst of 3
        self.gun_burst_interval = 0.08  # Time between burst shots
        self.gun_burst_shots_left = 0
        self.gun_burst_next_shot_time = 0
        self.last_projectile_time = time.time()

    def switch_form(self):
        now = time.time()
        if now - self.last_form_switch > self.form_switch_cooldown:
            self.form = 2 if self.form == 1 else 1
            self.last_form_switch = now

    def move(self, player_position, all_enemies):
        now = time.time()
        if self.form == 1:
            self.form_switch_cooldown = 5.0
        else:
            self.form_switch_cooldown = 3.0
        # Switch form every ~10 seconds, but bias choice by distance
        if now - self.last_form_switch > self.form_switch_cooldown:
            dx = self.position.x - player_position.x
            dz = self.position.z - player_position.z
            distance_to_player = math.sqrt(dx ** 2 + dz ** 2)
            # Probability: more likely to go to sword if close, gun if far
            if distance_to_player < 12.0:
                prob_gun = 0.2
            elif distance_to_player > 16.0:
                prob_gun = 0.8
            else:
                prob_gun = 0.5
            import random
            if random.random() < prob_gun:
                self.form = 2  # gun
            else:
                self.form = 1  # sword
            self.last_form_switch = now
        # ...existing code for movement...
        if self.form == 1:
            self.speed = self.sword_speed
            self.attack_range = self.sword_attack_range
            distance_to_player = math.sqrt(
                (self.position.x - player_position.x) ** 2 +
                (self.position.y - player_position.y) ** 2 +
                (self.position.z - player_position.z) ** 2
            )
            # Dash logic with windup and burst
            if not self.sword_dashing and not self.sword_dash_in_windup and distance_to_player < 10.0 and now - self.sword_last_dash > self.sword_dash_cooldown:
                self.sword_dash_in_windup = True
                self.sword_dash_windup_start = now
                # Use longer windup for first dash, slower for subsequent
                if self.sword_dash_count == 0:
                    self.sword_dash_windup = self.sword_dash_windup_first
                else:
                    self.sword_dash_windup = self.sword_dash_windup_repeat
                # Face the player
                direction = Vec3(
                    player_position.x - self.position.x,
                    0,
                    player_position.z - self.position.z
                ).normalize()
                self.sword_dash_direction = direction
            if self.sword_dash_in_windup:
                # Windup phase: do not move, but face the player
                if now - self.sword_dash_windup_start >= self.sword_dash_windup:
                    self.sword_dashing = True
                    self.sword_dash_in_windup = False
                    self.sword_dash_end_time = now + self.sword_dash_duration
                    self.sword_last_dash = now
            elif self.sword_dashing:
                # Dashing phase: move quickly in dash direction
                if self.sword_dash_direction is not None:
                    old_position = self.position
                    self.position = self.position + \
                        self.sword_dash_direction.scale(self.sword_dash_speed)
                    # Prevent getting stuck in wall after dash
                    if not self.is_position_clear(self.position, self.walls, radius=self.radius):
                        self.position = old_position
                        self.unstick_from_wall()
                if now >= self.sword_dash_end_time:
                    self.sword_dashing = False
                    self.sword_dash_direction = None
                    self.sword_dash_count += 1
            else:
                # Reset dash count if not dashing or winding up
                self.sword_dash_count = 0
                super().move(player_position, all_enemies)
                # After normal move, unstick if needed
                if not self.is_position_clear(self.position, self.walls, radius=self.radius):
                    self.unstick_from_wall()
        else:
            self.speed = self.gun_speed
            self.attack_range = self.gun_attack_range
            dx = self.position.x - player_position.x
            dz = self.position.z - player_position.z
            distance_to_player = math.sqrt(dx ** 2 + dz ** 2)
            preferred_distance = 18.0
            move_vec = Vec3(0, 0, 0)
            if distance_to_player < preferred_distance - 2.0:
                direction = Vec3(player_position.x - self.position.x,
                                 0, player_position.z - self.position.z).normalize()
                move_vec -= direction
            elif distance_to_player > preferred_distance + 2.0:
                direction = Vec3(player_position.x - self.position.x,
                                 0, player_position.z - self.position.z).normalize()
                move_vec += direction
            if move_vec.mag > 0.01:
                old_position = self.position
                move_vec = move_vec.normalize().scale(self.speed)
                self.position = self.position + move_vec
                # Prevent getting stuck in wall after move
                if not self.is_position_clear(self.position, self.walls, radius=self.radius):
                    self.position = old_position
                    self.unstick_from_wall()
            # Burst fire logic
            now = time.time()
            if self.gun_burst_shots_left > 0 and now >= self.gun_burst_next_shot_time:
                self.shoot_projectile_at_player(self.game, player_position)
                self.gun_burst_shots_left -= 1
                self.gun_burst_next_shot_time = now + self.gun_burst_interval
            elif distance_to_player < self.gun_attack_range and now - self.last_projectile_time > self.gun_projectile_cooldown:
                self.gun_burst_shots_left = self.gun_burst_count
                self.gun_burst_next_shot_time = now
                self.last_projectile_time = now

    def shoot_projectile_at_player(self, game, player_position):
        # Gun form: shoot a projectile at the player with bloom
        import random
        player_world_pos = player_position
        enemy_world_pos = self.position
        # Add bloom (random spread) to the projectile direction
        bloom_angle = 0.18  # radians, increase for more spread
        direction = Vec3(
            player_world_pos.x - enemy_world_pos.x,
            0,
            player_world_pos.z - enemy_world_pos.z
        ).normalize()
        # Randomly rotate direction by a small angle in xz plane
        angle = math.atan2(direction.z, direction.x)
        angle += random.uniform(-bloom_angle, bloom_angle)
        bloom_dir = Vec3(math.cos(angle), 0, math.sin(angle)).normalize()
        projectile_pos = Vec3(
            enemy_world_pos.x, enemy_world_pos.y + 2, enemy_world_pos.z)
        projectile_velocity = bloom_dir.scale(0.32)
        projectile = {
            "id": 4,
            "model": projectile_pos,
            "velocity": projectile_velocity,
            "program": game.sphere_program,
            "geometry": game.generate_sphere(0.4, 10, 10, position=Vec3(0, 0, 0)),
        }
        game.projectiles.append(projectile)
        game.objects.append(projectile)
        print("Miniboss shoots projectile at", player_world_pos)

    def attack_player(self, player_position):
        if self.form == 1:
            # Sword form: melee attack
            if self.is_player_in_sight(player_position):
                self.player.apply_damage(self.sword_attack_damage)
                print("Miniboss slashes player!")
        else:
            # Gun form: handled by shoot_projectile_at_player
            pass

    def get_form(self):
        return self.form


class FinalBoss(Enemy):
    def __init__(self, game, walls, enemy_walls, position=Vec3(0, 0, 0), health=2000, rotation=Vec3(0, 0, 0)):
        super().__init__(game, walls, enemy_walls, position, health, rotation)
        self.spawn_cooldown = 2.2  # seconds between spawns (phase 1, faster)
        self.last_spawn_time = time.time()
        self.max_minions = 5  # Max minions alive at once (phase 1, more)
        self.minion_type = 1  # 1: Enemy1, 2: Enemy2, 3: Enemy3
        self.radius = 2.5  # Larger collision for boss
        self.health = 200
        self.max_health = 200
        self.phase = 1
        self.stationary = True
        self.phase_transitioned = set()
        self.move_speed = 0.3  # Phase 3 movement speed
        self.flee_speed = 3  # Phase 2 and 3 flee speed
        self.target_pos = None
        self.last_move_time = time.time()
        self.move_cooldown = 0.01  # How often boss moves in phase 3
        self.fleeing = False
        self.flee_target = Vec3(36, -2, 0)  # Phase 2 flee
        self.flee_target2 = Vec3(34, -2, -84)  # Phase 3 first flee
        self.flee_target3 = Vec3(6, -2, -84)  # Phase 3 second flee (turn here)
        self.phase3_flee_state = 0  # 0: not started, 1: to target2, 2: to target3, 3: done
        self.fleeing = False

    def update_phase(self):
        # Phase transitions based on health
        if self.phase == 1 and self.health <= self.max_health * (2/3):
            self.phase = 2
            self.spawn_cooldown = 1.1  # Even faster spawns
            self.max_minions = 10
            self.stationary = True
            self.fleeing = True  # Start fleeing
            if 2 not in self.phase_transitioned:
                print("FinalBoss: Phase 2! Fleeing to new position.")
                self.phase_transitioned.add(2)
        if self.phase == 2 and self.health <= self.max_health * (1/3):
            self.phase = 3
            self.spawn_cooldown = 0.6  # Very fast spawns
            self.max_minions = 15
            self.stationary = True  # Stay stationary until double-flee is done
            self.phase3_flee_state = 1  # Start phase 3 double-flee
            if 3 not in self.phase_transitioned:
                print("FinalBoss: Phase 3! Double-flee before going mobile!")
                self.phase_transitioned.add(3)

    def move(self, player_position, all_enemies):
        self.update_phase()
        now = time.time()
        # Flee logic at start of phase 2
        if self.phase == 2 and self.fleeing:
            dx = self.flee_target.x - self.position.x
            dz = self.flee_target.z - self.position.z
            dist = math.sqrt(dx ** 2 + dz ** 2)
            if dist > 0.5:
                direction = Vec3(dx, 0, dz).normalize()
                if now - self.last_move_time > self.move_cooldown:
                    new_position = self.position + \
                        direction.scale(self.flee_speed)
                    ray_dir = (new_position - self.position).normalize()
                    ray_length = (new_position - self.position).mag
                    result, _ = raycast.raycast(
                        self.position, ray_dir, self.walls, ray_length=ray_length)
                    if not result:
                        self.position = new_position
                    self.last_move_time = now
                return  # Don't do anything else while fleeing
            else:
                self.fleeing = False  # Arrived at destination
        # Count minions spawned by this boss
        minion_count = sum(
            1 for enemy in self.game.enemies
            if hasattr(enemy["object"], "spawner_boss_id") and enemy["object"].spawner_boss_id is self
            and not enemy["object"].is_dead()
        )
        # Spawn minions if under cap and cooldown
        if minion_count < self.max_minions and now - self.last_spawn_time > self.spawn_cooldown:
            self.spawn_minion()
            self.last_spawn_time = now
        # Phase 3: double-flee sequence before going mobile (run this every frame in phase3_flee_state)
        if self.phase == 3:
            if self.phase3_flee_state == 1:
                # Go to flee_target2
                target = self.flee_target2
                dx = target.x - self.position.x
                dz = target.z - self.position.z
                dist = math.sqrt(dx ** 2 + dz ** 2)
                if dist > 0.5:
                    direction = Vec3(dx, 0, dz).normalize()
                    if now - self.last_move_time > self.move_cooldown:
                        step = min(self.flee_speed, dist)
                        new_position = self.position + direction.scale(step)
                        ray_dir = (new_position - self.position).normalize()
                        ray_length = (new_position - self.position).mag
                        result, _ = raycast.raycast(
                            self.position, ray_dir, self.walls, ray_length=ray_length)
                        if not result:
                            self.position = new_position
                        self.last_move_time = now
                    return
                else:
                    self.phase3_flee_state = 2  # Now go to target3
                    return
            elif self.phase3_flee_state == 2:
                # Go to flee_target3
                target = self.flee_target3
                dx = target.x - self.position.x
                dz = target.z - self.position.z
                dist = math.sqrt(dx ** 2 + dz ** 2)
                if dist > 0.5:
                    direction = Vec3(dx, 0, dz).normalize()
                    if now - self.last_move_time > self.move_cooldown:
                        step = min(self.flee_speed, dist)
                        new_position = self.position + direction.scale(step)
                        ray_dir = (new_position - self.position).normalize()
                        ray_length = (new_position - self.position).mag
                        result, _ = raycast.raycast(
                            self.position, ray_dir, self.walls, ray_length=ray_length)
                        # if not result:
                        #     self.position = new_position
                        self.position = new_position
                        self.last_move_time = now
                    return
                else:
                    self.phase3_flee_state = 3  # Done fleeing
                    self.stationary = False  # Now boss can move
                    # Turn to face player or a set direction
                    dx = player_position.x - self.position.x
                    dz = player_position.z - self.position.z
                    self.rotation = Vec3(0, math.atan2(dx, dz), 0)
                    return
        # Phase 3: mobile, chase player and enable face plant attack
        if self.phase == 3 and self.phase3_flee_state == 3 and not self.stationary:
            # Move toward player (xz plane)
            dx = player_position.x - self.position.x
            dz = player_position.z - self.position.z
            dist = math.sqrt(dx ** 2 + dz ** 2)
            if dist > 2.5:  # Don't overlap player
                direction = Vec3(dx, 0, dz).normalize()
                # Move only every move_cooldown seconds
                if now - self.last_move_time > self.move_cooldown:
                    new_position = self.position + \
                        direction.scale(self.move_speed)
                    # Raycast to avoid walking through walls
                    ray_dir = (new_position - self.position).normalize()
                    ray_length = (new_position - self.position).mag
                    result, _ = raycast.raycast(
                        self.position, ray_dir, self.walls, ray_length=ray_length)

                    self.position = new_position
                    self.last_move_time = now
            # Face plant attack logic (phase 3 only)
            face_plant_range = 4.0
            face_plant_cooldown = 5.0
            if not hasattr(self, 'last_face_plant_time'):
                self.last_face_plant_time = 0
            if dist <= face_plant_range and (now - self.last_face_plant_time > face_plant_cooldown):
                # Perform face plant attack
                print("FinalBoss: Face plant attack!")
                if hasattr(self.player, 'apply_damage'):
                    self.player.apply_damage(1)  # High damage
                self.last_face_plant_time = now
        # Optionally: add new attack patterns in phase 3
        # (e.g., area attack, projectile, etc.)

    def spawn_minion(self):
        # Alternate minion type for variety
        import numpy as np
        max_attempts = 12
        for attempt in range(max_attempts):
            offset = Vec3(np.random.uniform(-4, 4),
                          0, np.random.uniform(-4, 4))
            spawn_pos = self.position + offset
            if self.is_position_clear(spawn_pos, self.walls, radius=1.0):
                break
        else:
            spawn_pos = self.position
        # Use current game wall data for minion navigation
        current_walls = self.game.walls
        current_enemy_walls = getattr(self.game, 'enemy_walls', [])
        if self.minion_type == 1:
            minion = Enemy1(self.game, current_walls,
                            current_enemy_walls, spawn_pos, 100, returnhome=False)
            minion_type_int = 1
            self.minion_type = 2
        elif self.minion_type == 2:
            minion = Enemy2(self.game, current_walls,
                            current_enemy_walls, spawn_pos, 100, returnhome=False)
            minion_type_int = 2
            self.minion_type = 3
        else:
            minion = Enemy3(self.game, current_walls,
                            current_enemy_walls, spawn_pos, 200, returnhome=False)
            minion_type_int = 3
            self.minion_type = 1
        minion.spawner_boss_id = self
        # Add to game enemies list
        self.game.enemies.append({
            "name": f"boss_minion_{int(time.time()*1000)}",
            "type": minion_type_int,
            "room": 1,  # special room for boss
            "object": minion,
            "program": self.game.GLTF_program,
            "id": 10,
            "rotation": Vec3(0, 0, 0),
            "spawned": True,
        })
        # Add to objects and assign geometry immediately
        minion_dict = self.game.enemies[-1]
        if minion_type_int == 1:
            minion_dict["geometry"] = gltf_utils.load_gltf(
                self.game, self.game.enemy1_gltf, self.game.enemy1_bin_data, scale=Vec3(0.6, 0.6, 0.6))
        elif minion_type_int == 2:
            minion_dict["geometry"] = gltf_utils.load_gltf(
                self.game, self.game.enemy2_gltf, self.game.enemy2_bin_data, scale=Vec3(3, 3, 3))
        elif minion_type_int == 3:
            minion_dict["geometry"] = gltf_utils.load_gltf(
                self.game, self.game.enemy1_gltf, self.game.enemy1_bin_data, scale=Vec3(1.2, 0.7, 1.2))
        self.game.objects.append(minion_dict)

    def is_dead(self):
        return not self.is_alive

    # ...existing code...
