"""
Virtual roomba/vacuum AI project.
"""

# System Imports.
import sys
import sdl2.ext


# Module Variables.
# Here, we point to our image files to render to user.
RESOURCES = sdl2.ext.Resources(__file__, 'src/images/')
# Initialize window width/height.
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480


def main():
    """
    Project start.
    """
    # Initialize sdl2 library.
    sdl2.ext.init()

    # Initialize sprite factory, which is what draws our images (aka "sprites") to window.
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    # Initialize window and basic sprites.
    window = initialize_window(factory)

    # Force program to wait, so we actually see output.
    processor = sdl2.ext.TestEventProcessor()
    processor.run(window)

    # Call final library teardown logic.
    sdl2.ext.quit()


def initialize_window(factory):
    """
    Initializes render window for user.
    :param factory: SpriteFactory object which renders sprites to window.
    :return: Initialized window.
    """
    # Initialize render window.
    window = sdl2.ext.Window('CS 5820 - Virtual Roomba/Vacuum AI Project', size=(WINDOW_WIDTH, WINDOW_HEIGHT))
    window.show()

    # # Create single "sprite" to display.
    # sprite_background = factory.from_image(RESOURCES.get_path('background.png'))
    # sprite_background.x = window_center_w - 25
    # sprite_background.y = window_center_h - 25
    #
    # # Display sprites to window.
    # sprite_renderer = factory.create_sprite_render_system(window)
    # sprite_renderer.render(sprite_background)

    # Create sprite renderer factory.
    sprite_renderer = factory.create_sprite_render_system(window)

    # Calculate sprite counts to fit into rendered window.
    window_center_w = int(WINDOW_WIDTH / 2)
    window_center_h = int(WINDOW_HEIGHT / 2)
    sprite_w_count = int(WINDOW_WIDTH / 50) - 1
    sprite_h_count = int(WINDOW_HEIGHT / 50) - 1
    sprite_w_start = int(window_center_w - (int(sprite_w_count / 2) * 50))
    sprite_h_start = int(window_center_h - (int(sprite_h_count / 2) * 50))
    sprite_w_end = int(window_center_w + (int(sprite_w_count / 2) * 50))
    sprite_h_end = int(window_center_h + (int(sprite_h_count / 2) * 50))

    # Correct spacing if width sprite count is odd number.
    if (sprite_w_count % 2) == 1:
        sprite_w_start -= 25
        sprite_w_end -= 25

    # Correct spacing if height sprite count is odd number.
    if (sprite_h_count % 2) == 1:
        sprite_h_start -= 25
        sprite_h_end -= 25

    # Generate data structure dictionaries.
    window_data = {
        'total_pixel_w': WINDOW_WIDTH,
        'total_pixel_h': WINDOW_HEIGHT,
        'center_pixel_w': window_center_w,
        'center_pixel_h': window_center_h,
    }
    sprite_data = {
        'sprite_w_count': sprite_w_count,
        'sprite_h_count': sprite_h_count,
        'max_pixel_top': sprite_h_start,
        'max_pixel_right': sprite_w_end,
        'max_pixel_bottom': sprite_h_end,
        'max_pixel_left': sprite_w_start,
    }
    print('\n\n')
    print('window_data[total_pixel_w]: {0}'.format(window_data['total_pixel_w']))
    print('window_data[total_pixel_h]: {0}'.format(window_data['total_pixel_h']))
    print('window_data[center_pixel_w]: {0}'.format(window_data['center_pixel_w']))
    print('window_data[center_pixel_h]: {0}'.format(window_data['center_pixel_h']))
    print('sprite_data[sprite_w_count]: {0}'.format(sprite_data['sprite_w_count']))
    print('sprite_data[sprite_h_count]: {0}'.format(sprite_data['sprite_h_count']))
    print('sprite_data[max_pixel_top]: {0}'.format(sprite_data['max_pixel_top']))
    print('sprite_data[max_pixel_right]: {0}'.format(sprite_data['max_pixel_right']))
    print('sprite_data[max_pixel_bottom]: {0}'.format(sprite_data['max_pixel_bottom']))
    print('sprite_data[max_pixel_left]: {0}'.format(sprite_data['max_pixel_left']))
    print('\n\n')

    # Generate all sprite tiles.
    TileSet(factory, sprite_renderer, window_data, sprite_data)

    # Return generated window object.
    return window


class TileSet:
    """
    Holds set of all sprite tiles.
    """
    def __init__(self, sprite_factory, sprite_renderer, window_data, sprite_data):
        # Save class variables.
        self.sprite_renderer = sprite_renderer
        self.window_data = window_data
        self.sprite_data = sprite_data
        self.tile_set = []

        # Initialize all tiles.
        for row_index in range(sprite_data['sprite_h_count']):

            # Initialize row of tiles.
            curr_row = []
            y_coord = (row_index * 50) + sprite_data['max_pixel_top']

            # Initialize each tile in row.
            for col_index in range(sprite_data['sprite_w_count']):
                x_coord = (col_index * 50) + sprite_data['max_pixel_left']
                curr_row.append(Tile(sprite_factory, sprite_renderer, x_coord, y_coord, col_index, row_index))

            # Set full row to tile set.
            self.tile_set.append(curr_row)


class Tile:
    """
    A single tile, representing a single location in the environment.
    """
    def __init__(self, sprite_factory, sprite_renderer, window_x_coord, window_y_coord, row_index, col_index):
        self.renderer = sprite_renderer
        self.row_index = row_index
        self.col_index = col_index
        self.x = window_x_coord
        self.y = window_y_coord

        # Render self to window.
        sprite_background = sprite_factory.from_image(RESOURCES.get_path('background.png'))
        sprite_background.x = self.x
        sprite_background.y = self.y
        sprite_renderer.render(sprite_background)


if __name__ == '__main__':
    print('Starting program.')

    main()

    print('Terminating program.')

