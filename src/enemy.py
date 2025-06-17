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
                self.position = self.position + move_vec
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
                self.position += direction_to_return.scale(self.speed)
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
        print("Enemy has died")
        self.is_alive = False

    def is_dead(self):
        return not self.is_alive


class Enemy1(Enemy):
    def __init__(self, game, walls, enemy_walls, position=Vec3(0, 0, 0), health=100, rotation=Vec3(0, 0, 0)):
        super().__init__(game, walls, enemy_walls, position, health, rotation)

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
                self.position = self.position + move_vec
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
                self.position += direction_to_return.scale(self.speed)
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
        print("Enemy has died")
        self.is_alive = False

    def is_dead(self):
        return not self.is_alive


class Enemy2(Enemy):
    def __init__(self, game, walls, enemy_walls, position=Vec3(0, 0, 0), health=100, rotation=Vec3(0, 0, 0)):
        super().__init__(game, walls, enemy_walls, position, health, rotation)
        self.game = game
        self.health = 60
        self.max_health = 60
        
        self.return_position = position  # Store original position
        
        self.speed = 0.1 # Override speed for Enemy2
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
            # Return to original position if not already there
            if self.position != self.return_position:
                direction_to_return = Vec3(
                    self.return_position.x - self.position.x,
                    0,
                    self.return_position.z - self.position.z
                )
                if direction_to_return.mag > 0.1:
                    direction_to_return = direction_to_return.normalize()
                    new_position = self.position + direction_to_return.scale(self.speed)
                    # Raycast from current to new position to check for wall collision
                    ray_dir = (new_position - self.position).normalize()
                    ray_length = (new_position - self.position).mag
                    result, _ = raycast.raycast(self.position, ray_dir, self.walls, ray_length=ray_length)
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
            result, _ = raycast.raycast(self.position, ray_dir, self.walls, ray_length=ray_length)
            if not result:
                # Check if new_position is too close to any wall; if so, do not move
                too_close_to_wall = False
                for wall in self.walls:
                    if "buffer_data" in wall:
                        positions = wall["buffer_data"]
                        num_vertices = len(positions) // 5
                        for i in range(num_vertices):
                            wall_pos = Vec3(positions[i*5], 0, positions[i*5+2])
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
        projectile_pos = Vec3(enemy_world_pos.x, enemy_world_pos.y + 2, enemy_world_pos.z)
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
    def __init__(self, game, walls, enemy_walls, position=Vec3(0, 0, 0), health=300, rotation=Vec3(0, 0, 0)):
        # 3x tankier than Enemy1 (default health=100)
        super().__init__(game, walls, enemy_walls, position, health, rotation)
        self.speed = 0.02
        self.normal_speed = 0.05  # Store normal speed
        self.slow_speed = 0.05   # Same as normal speed
        self.health = 500  # Increased health
        self.max_health = 500
