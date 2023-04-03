import json
import random
import pygame
import esper

from src.create.prefabs_creator import create_square_entity
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(world: esper.World, delta_time: float):
    components = world.get_components(CEnemySpawner)
    for entity, (enemy_spawner,) in components:
        enemy_spawner.current_event_time -= delta_time
        if enemy_spawner.current_event_time <= 0:
            if enemy_spawner.current_event_index < len(enemy_spawner.spawn_events):
              # Create enemy entity using spawn event data
              spawn_event = enemy_spawner.spawn_events[enemy_spawner.current_event_index]
              # Load enemy type configuration from file
              with open('assets/cfg/enemies.json', 'r') as f:
                  enemies_config = json.load(f)
                  enemy_type = enemies_config[spawn_event.enemy_type]
              # Create enemy entity
              create_square_entity(
                  world,
                  pygame.Vector2(enemy_type['size']['x'],
                                enemy_type['size']['y']),
                  spawn_event.position,
                  pygame.Vector2(random.uniform(enemy_type['velocity_min'], enemy_type['velocity_max']),
                                random.uniform(enemy_type['velocity_min'], enemy_type['velocity_max'])),
                  pygame.Color(
                      enemy_type['color']['r'], enemy_type['color']['g'], enemy_type['color']['b'])
              )
              # Move to next spawn event
              enemy_spawner.current_event_index += 1
              if enemy_spawner.current_event_index >= len(enemy_spawner.spawn_events):
                  world.delete_entity(entity)
              else:
                  enemy_spawner.current_event_time = enemy_spawner.spawn_events[
                      enemy_spawner.current_event_index].spawn_time
