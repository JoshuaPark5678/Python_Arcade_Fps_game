import arcade
import arcade.resources
from pyglet.math import Vec3
from array import array
from arcade.gl import BufferDescription
from pygltflib import GLTF2
import numpy as np
import os
import math

import raycast

class Enemy():
    def __init__(self, walls, enemy_walls, position = Vec3(0, 0, 0), health = 100, rotation = Vec3(0, 0, 0)):
        self.is_alive = True
        
        self.position = position
        self.return_position = position
        self.speed = 0.1
        
        self.health = health
        self.rotation = rotation
        
        self.walls = []
        for wall in walls: 
            wall["id"] = 1  # Assign id = 1 to each wall
            self.walls.append(wall)
        for wall in enemy_walls:
            wall["id"] = 1
            self.walls.append(wall)

        self.proximity_radius = 40.0  # Distance within which the enemy will detect the player

    def move(self, player_position):
        # Check if player is within a certain distance
        distance_to_player = math.sqrt(
            (self.position.x - player_position.x) ** 2 +
            (self.position.y - player_position.y) ** 2 +
            (self.position.z - player_position.z) ** 2
        )
        
        
        if distance_to_player < self.proximity_radius and distance_to_player > 3.0 and self.is_player_in_sight(player_position):
            # find player direction
            forward = Vec3(
                math.sin(self.rotation.y), 0, math.cos(self.rotation.y)).scale(self.speed)
            self.position += forward
        else:
            # If player is not in sight, return to original position
            if self.position != self.return_position:
                direction_to_return = Vec3(
                    self.return_position.x - self.position.x,
                    self.return_position.y - self.position.y,
                    self.return_position.z - self.position.z
                ).normalize()
                self.position += direction_to_return.scale(self.speed)
                
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

        return not raycast.raycast(ray_start, ray_direction, self.walls, distance_to_player)

    def get_world_position(self):
        return self.position
    
    def get_health(self):
        return self.health
    
    def get_rotation(self):
        return self.rotation

    def apply_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
    
    def die(self):
        print("Enemy has died")
        self.is_alive = False
        
    def is_dead(self):
        return not self.is_alive