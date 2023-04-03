


import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def create_square_entity(ecs_world: esper.World, size: pygame.Vector2, pos: pygame.Vector2, vel: pygame.Vector2, color: pygame.Color):
    square_entity = ecs_world.create_entity()
    ecs_world.add_component(square_entity, CSurface(size=size, color=color))
    ecs_world.add_component(square_entity, CTransform(pos=pos))
    ecs_world.add_component(square_entity, CVelocity(vel=vel))
    return square_entity