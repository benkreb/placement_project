import numpy as np
import trimesh
import matplotlib.pyplot as plt
import json
import random

# Load the STL file
city_model = trimesh.load_mesh('city_model.stl')

# Read streetlamp positions from a JSON file
with open('street_lamp_positions.json', 'r') as json_file:
    lamp_positions = json.load(json_file)

# Select 5 random positions for modules
random_module_positions = random.sample(lamp_positions, 5)

# Remove the selected module positions from the list to select a unique position for the gateway
remaining_positions = [pos for pos in lamp_positions if pos not in random_module_positions]

# Select 1 random position for the gateway
random_gateway_position = random.choice(remaining_positions)

# Convert the selected module positions into a numpy array
module_positions = np.array([[pos['x'], pos['y'], pos['z']] for pos in random_module_positions])

# Convert the gateway position into a numpy array
gateway_position = np.array([random_gateway_position['x'], random_gateway_position['y'], random_gateway_position['z']])

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

# Plot the gateway position
ax.scatter(gateway_position[0], gateway_position[1], gateway_position[2], color='r', s=200, label='Gateway', marker='*')

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
print("Randomly selected gateway position:")
print(gateway_position)

# Save the selected positions to a JSON file
selected_positions = {
    'modules': [{'x': pos[0], 'y': pos[1], 'z': pos[2]} for pos in module_positions],
    'gateway': {'x': gateway_position[0], 'y': gateway_position[1], 'z': gateway_position[2]}
}

with open('selected_module_positions.json', 'w') as output_file:
    json.dump(selected_positions, output_file, indent=4)

print("Selected module and gateway positions saved to 'selected_module_positions.json'")
