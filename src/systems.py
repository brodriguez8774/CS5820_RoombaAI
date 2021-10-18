"""
World system definitions.
These are subsystems added to the "world manager" object, that basically control actions being taken on each event tick.
"""

# System Imports.
import sdl2.ext

# User Imports.
from src.entities.system_entities import Movement


class SoftwareRendererSystem(sdl2.ext.SoftwareSpriteRenderSystem):
    """
    System that handles displaying sprites to renderer window.
    """
    def __init__(self, window):
        super(SoftwareRendererSystem, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRendererSystem, self).render(components)


class MovementSystem(sdl2.ext.Applicator):
    """
    System that handles movement of entities.
    """
    def __init__(self, data_manager, min_x, min_y, max_x, max_y):
        # Call parent logic.
        super().__init__()

        # Save component types values. Necessary for SDL2 system handling.
        self.componenttypes = Movement, sdl2.ext.Sprite

        # Save class variables.
        self.data_manager = data_manager
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def process(self, world, componenttypes):
        for movement_tick, sprite in componenttypes:
            # Get sprite size in pixels.
            sprite_width, sprite_height = sprite.size

            # Check if any movement directions are active for tick.
            if movement_tick.north:
                # Move north (upward).
                sprite.y -= 50
            elif movement_tick.east:
                # Move east (right).
                sprite.x += 50
            elif movement_tick.south:
                # Move south (down).
                sprite.y += 50
            elif movement_tick.west:
                # Move west (left).
                sprite.x -= 50

            # Reset movement tick values, now that we've handled for them.
            movement_tick.north = False
            movement_tick.east = False
            movement_tick.south = False
            movement_tick.west = False

            # For below, we verify that sprite's new location is within bounds.
            # We use the more restrictive of either "the provided limit class limit" or "defined window limit".

            # Verify that sprite is still within north (upper) screen bounds.
            north_max = max(self.min_x, self.data_manager.sprite_data['max_pixel_north'])
            sprite.y = max(north_max, sprite.y)

            # Verify that sprite is still within east (right) screen bounds.
            sprite_right = sprite.x + sprite_width
            east_max = min(self.max_x, self.data_manager.sprite_data['max_pixel_east'])
            if sprite_right > east_max:
                sprite.x = east_max - sprite_width

            # Verify that sprite is still within south (bottom) screen bounds.
            sprite_lower = sprite.y + sprite_height
            south_max = min(self.max_y, self.data_manager.sprite_data['max_pixel_south'])
            if sprite_lower > south_max:
                sprite.y = south_max - sprite_height

            # Verify that sprite is still within west (left) screen bounds.
            west_max = max(self.min_x, self.data_manager.sprite_data['max_pixel_west'])
            sprite.x = max(west_max, sprite.x)