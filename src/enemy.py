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
import main

class Enemy():
    def __init__(self, position = Vec3(0, 0, 0), health = 100, rotation = Vec3(0, 0, 0), walls = [], bounding_box = []):
        self.position = position
        self.return_position = position
        self.speed = 0.1
        
        self.health = health
        self.rotation = rotation

        self.bounding_box = bounding_box
        self.walls = walls
        
        self.proximity_radius = 20.0  # Distance within which the enemy will detect the player

    def move(self, player_position):
        # Check if player is within a certain distance
        distance_to_player = math.sqrt(
            (self.position.x + player_position.x) ** 2 +
            (self.position.y + player_position.y) ** 2 +
            (self.position.z + player_position.z) ** 2
        )
        print(f"Distance to player: {distance_to_player}")
        if distance_to_player < self.proximity_radius and distance_to_player > 3.0:
            # find player direction
            forward = Vec3(
                math.sin(self.rotation.y), 0, math.cos(self.rotation.y)).scale(self.speed)
            self.position += forward
        
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def get_world_position(self):
        return self.position
    
    def get_health(self):
        return self.health
    
    def get_rotation(self):
        return self.rotation

    def die(self):
        print("Enemy has died")