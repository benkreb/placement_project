import numpy as np
import trimesh
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import json

# Load the STL file
city_model = trimesh.load_mesh('blank_city.stl')


# Function to identify potential street lamps
def identify_street_lamps(mesh, height_threshold=2.0, width_threshold=0.2):
    # Identify vertices above the height threshold
    high_vertices = mesh.vertices[mesh.vertices[:, 2] > height_threshold]

    # Cluster the high vertices to find potential lamp tops
    clustering = DBSCAN(eps=width_threshold, min_samples=1).fit(high_vertices)
    labels = clustering.labels_

    # Calculate the center point of each cluster
    unique_labels = set(labels)
    lamp_centers = np.array([high_vertices[labels == label].mean(axis=0) for label in unique_labels])

    return lamp_centers


# Identify potential street lamp positions
potential_lamps = identify_street_lamps(city_model)

# Extract vertices and faces for visualization
vertices = city_model.vertices
faces = city_model.faces

# Visualize the STL file with identified street lamp positions
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the mesh
ax.plot_trisurf(vertices[:, 0], vertices[:, 1], vertices[:, 2], triangles=faces, cmap='viridis', edgecolor='none')

# Plot the identified street lamp positions
ax.scatter(potential_lamps[:, 0], potential_lamps[:, 1], potential_lamps[:, 2], color='r', s=100)

# Set labels for axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

# Output the identified street lamp positions
print("Identified street lamp positions:")
print(potential_lamps)

# Convert positions to a list of dictionaries
lamp_positions = [{'x': float(pos[0]), 'y': float(pos[1]), 'z': float(pos[2])} for pos in potential_lamps]

# Save the positions to a JSON file
with open('street_lamp_positions.json', 'w') as json_file:
    json.dump(lamp_positions, json_file, indent=4)

print("Street lamp positions have been saved to street_lamp_positions.json")
