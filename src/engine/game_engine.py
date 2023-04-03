import esper
import pygame
import json
import pdb


from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_debounce import system_screen_bounce
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.components.c_spawn_event_data import SpawnEventData
from src.ecs.components.c_enemy_spawner import CEnemySpawner

class GameEngine:
    def __init__(self) -> None:
        pygame.init()

        # Leer valores de pantalla desde archivo JSON
        with open('assets/cfg/window.json', 'r') as f:
            window_config = json.load(f)['window']
        
        self._screen = pygame.display.set_mode((window_config['size']['w'], window_config['size']['h']), pygame.SCALED)
        pygame.display.set_caption(window_config['title'])
        self._clock = pygame.time.Clock()
        self.is_running = False
        self.frame_rate = window_config['framerate']
        self.delta_time = 0
        self.ecs_world = esper.World()
        self.screen_color = pygame.Color(window_config['bg_color']['r'], window_config['bg_color']['g'], window_config['bg_color']['b'])

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        # Crear entidad de spawner
        enemy_spawner = self.ecs_world.create_entity()
        # Cargar eventos de spawn desde archivo JSON
        with open('assets/cfg/level_01.json', 'r') as f:
            level_data = json.load(f)

        spawn_events = []
        for spawn_event_data in level_data['enemy_spawn_events']:
            enemy_type = spawn_event_data['enemy_type']
            time = spawn_event_data['time']
            position = pygame.Vector2(spawn_event_data['position']['x'], spawn_event_data['position']['y'])
            spawn_event = SpawnEventData(enemy_type, time, position)
            spawn_events.append(spawn_event)

        # Agregar componente CEnemySpawner a la entidad
        self.ecs_world.add_component(enemy_spawner, CEnemySpawner(spawn_events))

    def _calculate_time(self):
        self._clock.tick(self.frame_rate)
        self.delta_time = self._clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        # Avanzar en x con a 100 pixeles por segundo
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self._screen)
        system_enemy_spawner(self.ecs_world, self.delta_time)

    def _draw(self):
        self._screen.fill(self.screen_color)
        system_rendering(self.ecs_world, self._screen)
        pygame.display.flip()   # update the display

    def _clean(self):
        pygame.quit()
