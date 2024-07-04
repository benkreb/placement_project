import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh
from scipy.spatial import cKDTree


def generate_building(x, y, width, depth, height):
    vertices = [
        [x, y, 0], [x + width, y, 0], [x + width, y + depth, 0], [x, y + depth, 0],  # bottom
        [x, y, height], [x + width, y, height], [x + width, y + depth, height], [x, y + depth, height]  # top
    ]
    faces = [
        [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7],  # sides
        [0, 1, 2, 3], [4, 5, 6, 7]  # bottom, top
    ]
    return vertices, faces, width, depth, height


def check_collision(new_building, tree, buildings):
    new_x, new_y, new_width, new_depth = new_building[0][0][0], new_building[0][0][1], new_building[2], new_building[3]
    new_center = np.array([new_x + new_width / 2, new_y + new_depth / 2])

    if tree is not None:
        distances, indices = tree.query(new_center, k=1)
        closest_building = buildings[indices]
        closest_x, closest_y, closest_width, closest_depth = closest_building[0][0][0], closest_building[0][0][1], \
        closest_building[2], closest_building[3]

        if not (
                new_x + new_width < closest_x or new_x > closest_x + closest_width or new_y + new_depth < closest_y or new_y > closest_y + closest_depth):
            return True
    return False


def generate_city(width, depth, num_buildings):
    city = []
    centers = []
    tree = None

    while len(city) < num_buildings:
        x = random.uniform(0, width - 10)
        y = random.uniform(0, depth - 10)
        building_width = random.uniform(5, 10)
        building_depth = random.uniform(5, 10)
        building_height = random.uniform(10, 20)
        new_building = generate_building(x, y, building_width, building_depth, building_height)

        if not check_collision(new_building, tree, city):
            city.append(new_building)
            centers.append([x + building_width / 2, y + building_depth / 2])
            tree = cKDTree(centers)

    return city


def plot_city(city):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for building in city:
        vertices, faces, _, _, _ = building
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        ax.add_collection3d(
            Poly3DCollection(mesh.triangles, alpha=0.3, facecolor='cyan', linewidths=0.1, edgecolor='r'))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)
    ax.set_zlim(0, 50)

    plt.show()


def save_city(city, filename):
    meshes = []
    for building in city:
        vertices, faces, _, _, _ = building
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        meshes.append(mesh)

    combined = trimesh.util.concatenate(meshes)
    combined.export(filename)

def main():
    city_width = 50
    city_depth = 50
    num_buildings = 3
    city = generate_city(city_width, city_depth, num_buildings)
    plot_city(city)
    save_city(city, 'generated_city.stl')

if __name__ == '__main__':
    main()