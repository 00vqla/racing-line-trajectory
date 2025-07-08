import numpy as np
import matplotlib.pyplot as plt

# quarter circle track
radius = 50  
num_points = 100  

# generate corner
theta = np.linspace(0, np.pi/2, num_points)
x = radius * np.cos(theta)
y = radius * np.sin(theta)

# plotting track
plt.figure(figsize=(6,6))
plt.plot(x, y, label='Track (90-degree corner)')
plt.xlabel('x (meters)')
plt.ylabel('y (meters)')
plt.title('Simple 90-degree Corner Track')
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()

# car param
car = {
    'mass': 1200,         # kg
    'max_lateral_g': 1.0, # max cornering grip in g
    'max_accel': 3.0,     # m/s^2, max acceleration
    'max_brake': 6.0      # m/s^2, max braking
}

print("car parameters:", car)