import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform


def system_screen_bounce(world: esper.World, screen: pygame.Surface) -> None:
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface)

    c_transform: CTransform
    c_velocity: CVelocity
    c_surface: CSurface

    for ent, (c_transform, c_velocity, c_surface) in components:
        # Bounce on screen
        square_rect = c_surface.surf.get_rect(topleft=c_transform.pos)

        if square_rect.left <= 0 or square_rect.right >= screen_rect.right:
            c_velocity.vel.x *= -1
            square_rect.clamp_ip(screen_rect)
            c_transform.pos.x = square_rect.x

        if square_rect.top <= 0 or square_rect.bottom >= screen_rect.bottom:
            c_velocity.vel.y *= -1
            square_rect.clamp_ip(screen_rect)
            c_transform.pos.y = square_rect.y
