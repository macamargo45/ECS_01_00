import pygame
from typing import List

from src.ecs.components.c_spawn_event_data import SpawnEventData

class CEnemySpawner:
    def __init__(self, spawn_events: List[SpawnEventData]):
        self.spawn_events = spawn_events
        self.current_event_index = 0
        self.current_event_time = self.spawn_events[0].spawn_time
