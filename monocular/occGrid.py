import numpy as np

def create_occupancy_grid(free_space_map, grid_x=20, grid_y=6, cell_size=0.25):
    # Number of cells in the grid
    cells_x = int(grid_x / cell_size)
    cells_y = int(grid_y / cell_size)

    # Initialize the occupancy grid to zero
    occupancy_grid = np.zeros((cells_y, cells_x))

    # TODO: Fill in the occupancy grid based on the bird's-eye view image (free_space_map)
    # For example, you can loop through each cell and fill in the occupancy probability

    return occupancy_grid