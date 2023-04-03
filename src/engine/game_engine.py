import esper
import pygame
from src.create.prefabs_creator import create_square_entity

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_debounce import system_screen_bounce


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((640, 360), pygame.SCALED)
        self._clock = pygame.time.Clock()
        self.is_running = False
        self.frame_rate = 60
        self.delta_time = 0
        self.ecs_world = esper.World()

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
        create_square_entity(self.ecs_world, pygame.Vector2(50, 50), pygame.Vector2(150, 300), pygame.Vector2(-200, 300), pygame.Color(255, 0, 0))

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

    def _draw(self):
        self._screen.fill((0, 200, 128))
        system_rendering(self.ecs_world, self._screen)
        pygame.display.flip()   # update the display

    def _clean(self):
        pygame.quit()
