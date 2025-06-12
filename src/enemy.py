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
    def __init__(self, player, walls, enemy_walls, position=Vec3(0, 0, 0), health=100, rotation=Vec3(0, 0, 0)):
        self.is_alive = True

        self.player = player
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

            # Check collision with other enemies
            for other in all_enemies:
                if other["object"] is self or other["object"].is_dead():
                    continue
                distance = (new_position - other["object"].position).mag
                if distance < self.radius * 2:  # or self.radius + other.radius
                    # Collision detected, don't move
                    return

            # If no collision, update position
            self.position = new_position
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
