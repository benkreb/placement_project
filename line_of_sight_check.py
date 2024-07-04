import trimesh
import numpy as np
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Function to check if there's a clear line of sight between two points
def check_line_collision(mesh, point1, point2):
    ray_origins = np.array([point1])
    ray_directions = np.array([point2 - point1])
    ray_directions /= np.linalg.norm(ray_directions)  # Normalize the direction

    intersections = mesh.ray.intersects_location(ray_origins=ray_origins, ray_directions=ray_directions)
    return len(intersections[0]) > 0

# Function to plot city, modules, and lines of sight
def plot_city_and_modules_with_los(mesh, modules, los_matrix):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the city buildings
    for face in mesh.faces:
        triangle = mesh.vertices[face]
        poly = Poly3DCollection([triangle])
        poly.set_color('cyan')
        poly.set_alpha(0.3)
        ax.add_collection3d(poly)

    # Plot the communication modules
    for module in modules:
        ax.scatter(module[0], module[1], module[2], color='red', s=100)
        ax.text(module[0], module[1], module[2], f'({module[0]:.1f}, {module[1]:.1f}, {module[2]:.1f})', color='black')

    # Plot the lines of sight
    for i in range(len(modules)):
        for j in range(i + 1, len(modules)):
            color = 'green' if los_matrix[i][j] else 'red'
            ax.plot([modules[i][0], modules[j][0]],
                    [modules[i][1], modules[j][1]],
                    [modules[i][2], modules[j][2]],
                    color=color)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(mesh.bounds[0][0], mesh.bounds[1][0])
    ax.set_ylim(mesh.bounds[0][1], mesh.bounds[1][1])
    ax.set_zlim(mesh.bounds[0][2], mesh.bounds[1][2])

    plt.show()

def main():
    # Load the city mesh
    mesh = trimesh.load('generated_city.stl')

    # Load the module positions
    with open('module_positions.json', 'r') as f:
        modules = np.array(json.load(f))

    # Initialize line of sight matrix
    num_modules = len(modules)
    los_matrix = np.zeros((num_modules, num_modules), dtype=bool)

    # Check line of sight between modules
    for i in range(num_modules):
        for j in range(i + 1, num_modules):
            point1 = modules[i]
            point2 = modules[j]
            if not check_line_collision(mesh, point1, point2):
                print(f"Clear line of sight between module {i+1} and module {j+1}.")
                los_matrix[i][j] = True
                los_matrix[j][i] = True
            else:
                print(f"No line of sight between module {i+1} and module {j+1}.")
                los_matrix[i][j] = False
                los_matrix[j][i] = False

    # Plot the city with modules and lines of sight
    plot_city_and_modules_with_los(mesh, modules, los_matrix)

if __name__ == '__main__':
    main()
