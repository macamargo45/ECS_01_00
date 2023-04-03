import pygame
import esper

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform


def system_movement(world: esper.World, delta_time: float) -> None:
    components = world.get_components(CTransform, CVelocity)

    c_transform: CTransform
    c_velocity: CVelocity

    for ent, (c_transform, c_velocity) in components:
        # Avanzar en x con a 100 pixeles por segundo
        c_transform.pos.x += c_velocity.vel.x * delta_time
        c_transform.pos.y += c_velocity.vel.y * delta_time
