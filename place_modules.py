import trimesh
import numpy as np
import random
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# Function to check collision with buildings


def check_collision(position, mesh):
    # Creating a small box around the position to simulate the module
    box_size = 0.5
    module_box = trimesh.creation.box(extents=[box_size, box_size, box_size])
    module_box.apply_translation(position)

    # We need to cast rays in multiple directions to ensure no part of the box intersects with the mesh
    directions = np.array([
        [1, 0, 0], [-1, 0, 0],
        [0, 1, 0], [0, -1, 0],
        [0, 0, 1], [0, 0, -1]
    ])
    ray_origins = np.array([position] * len(directions))

    # Check for intersections with the mesh (city)
    intersections = mesh.ray.intersects_any(ray_origins=ray_origins, ray_directions=directions)
    return np.any(intersections)


# Function to place communication modules avoiding collisions


def place_modules(mesh, num_modules=3):
    min_bound, max_bound = mesh.bounds
    modules = []
    while len(modules) < num_modules:
        x = random.uniform(min_bound[0], max_bound[0])
        y = random.uniform(min_bound[1], max_bound[1])
        z = random.uniform(min_bound[2], max_bound[2])
        position = np.array([x, y, z])
        if not check_collision(position, mesh):
            modules.append(position)
    return np.array(modules)


# Function to create colored spheres for modules


def create_colored_spheres(modules, radius=1.0):
    spheres = []
    for i, module in enumerate(modules):
        sphere = trimesh.creation.icosphere(subdivisions=3, radius=radius)
        sphere.apply_translation(module)
        red_color = [255, 0, 0, 255]  # RGBA format
        sphere.visual.vertex_colors = np.array([red_color] * len(sphere.vertices))
        spheres.append(sphere)
    return trimesh.util.concatenate(spheres)


# Function to plot city with placed modules


def plot_city_with_modules(mesh, modules):
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

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(mesh.bounds[0][0], mesh.bounds[1][0])
    ax.set_ylim(mesh.bounds[0][1], mesh.bounds[1][1])
    ax.set_zlim(mesh.bounds[0][2], mesh.bounds[1][2])

    plt.show()


# Main function for module placement


def main():
    # Load the STL file
    mesh = trimesh.load('generated_city.stl')

    # Place communication modules
    modules = place_modules(mesh, num_modules=3)
    print("Module positions:")
    print(modules)

    # Save module positions to a JSON file
    with open('module_positions.json', 'w') as f:
        json.dump(modules.tolist(), f)

    # Create colored spheres for the modules
    spheres = create_colored_spheres(modules)

    # Combine the original mesh with the spheres
    updated_mesh = mesh + spheres

    # Save the updated mesh to a PLY file (which supports color)
    updated_mesh.export('city_with_modules.ply')

    # Plot the city with modules
    plot_city_with_modules(mesh, modules)


if __name__ == '__main__':
    main()
