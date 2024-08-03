



s



import matplotlib.pyplot as plt
import numpy as np
import sys

class SpacecraftSwarm:
    def __init__(self, num_spacecraft, mode=None):
        self.num_spacecraft = num_spacecraft
        self.spacecraft_size = 0.1  # Diameter in units
        self.spacecraft_speed = 0.01  # Movement speed
        self.communication_range = 2.0
        self.sensing_range = 1.5
        self.num_iterations = 2000  # Increased number of iterations
        self.spacecraft_positions = None
        self.communication_links = None
        try:
            self.spacecraft_positions = self.initialize_positions(mode)
            self.communication_links = np.zeros((num_spacecraft, num_spacecraft))
        except Exception as e:
            print("Error:", e)
            print("Exiting...")
            sys.exit(1)

    def initialize_positions(self, mode):
        if mode == "grid":
            side_length = int(np.sqrt(self.num_spacecraft))
            positions = np.array([(i % side_length, i // side_length) for i in range(self.num_spacecraft)], dtype=float)
            positions *= 0.5  # Adjust for spacing
            return positions
        elif mode == "circle":
            theta = np.linspace(0, 2*np.pi, self.num_spacecraft)
            positions = np.array([np.cos(theta), np.sin(theta)]).T * 0.4  # Adjust for radius
            return positions
        else:
            raise ValueError("Invalid mode. Available modes: 'grid', 'circle'")

    def update_positions(self):
        movement = np.random.randn(self.num_spacecraft, 2) * self.spacecraft_speed
        self.spacecraft_positions += movement
        self.spacecraft_positions %= 1

    def update_communication_links(self):
        distances = np.linalg.norm(self.spacecraft_positions[:, None, :] - self.spacecraft_positions[None, :, :], axis=2)
        self.communication_links = (distances < self.communication_range).astype(int)

    def plot(self, t):
        plt.clf()
        plt.title(f"Spacecraft Swarm Simulation (Iteration {t})")
        for i in range(self.num_spacecraft):
            for j in range(i + 1, self.num_spacecraft):
                if self.communication_links[i, j]:
                    plt.plot([self.spacecraft_positions[i, 0], self.spacecraft_positions[j, 0]],
                             [self.spacecraft_positions[i, 1], self.spacecraft_positions[j, 1]], 'b-', alpha=0.3)
            circle = plt.Circle(self.spacecraft_positions[i], self.spacecraft_size / 2, color='r', fill=False)
            plt.gca().add_artist(circle)

        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.grid(True)
        plt.pause(0.01)


def graceful_exit():
    print("\nExiting gracefully...")
    sys.exit(0)

try:
    print("Select mode:")
    print("1. Grid")
    print("2. Circle")
    print("0. Exit")
    mode_choice = input("Enter mode choice (0 to exit, 1 for Grid, 2 for Circle): ")

    if mode_choice == "0":
        graceful_exit()

    if mode_choice not in ["1", "2"]:
        raise ValueError("Invalid choice. Please enter 1, 2, or 0.")

    num_spacecraft = 36  # Increased number of spacecraft
    mode = "grid" if mode_choice == "1" else "circle"

    # Initialize spacecraft swarm with selected mode
    swarm = SpacecraftSwarm(num_spacecraft=num_spacecraft, mode=mode)

    # Initialize figure
    plt.figure()

    # Simulation loop
    for t in range(swarm.num_iterations):
        swarm.update_positions()
        swarm.update_communication_links()
        swarm.plot(t)

    plt.show()

except KeyboardInterrupt:
    graceful_exit()

except Exception as e:
    print("Error:", e)
    graceful_exit()
