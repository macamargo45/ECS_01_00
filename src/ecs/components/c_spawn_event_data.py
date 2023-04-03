import pygame

class SpawnEventData:
    def __init__(self, enemy_type: str, spawn_time: float, position: pygame.Vector2):
        self.enemy_type = enemy_type
        self.spawn_time = spawn_time
        self.position = position