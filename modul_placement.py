import numpy as np
import trimesh
import matplotlib.pyplot as plt
import json
import random

# Load the STL file
city_model = trimesh.load_mesh('city_model.stl')

# Read street lamp positions from a JSON file
with open('street_lamp_positions.json', 'r') as json_file:
    lamp_positions = json.load(json_file)

# Select 5 random positions
random_lamp_positions = random.sample(lamp_positions, 5)

# Convert the selected positions into a numpy array
module_positions = np.array([[pos['x'], pos['y'], pos['z']] for pos in random_lamp_positions])

# Extract vertices and faces from the existing STL file
vertices = city_model.vertices
faces = city_model.faces

# Visualize the STL file and module positions
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the mesh
ax.plot_trisurf(vertices[:, 0], vertices[:, 1], vertices[:, 2], triangles=faces, cmap='viridis', edgecolor='none')

# Plot the street lamp positions
ax.scatter(module_positions[:, 0], module_positions[:, 1], module_positions[:, 2], color='b', s=100, label='Modules')

# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

# Show the plot
plt.show()

# Print the randomly selected positions
print("Randomly selected module positions:")
print(module_positions)
