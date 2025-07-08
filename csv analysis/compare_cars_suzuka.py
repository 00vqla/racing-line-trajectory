import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Load Suzuka track data ---
track = pd.read_csv('MoscowRaceway.csv', comment='#', header=None, names=['x_m', 'y_m', 'w_tr_right_m', 'w_tr_left_m'])
x = np.array(track['x_m'])
y = np.array(track['y_m'])
w_tr_right = np.array(track['w_tr_right_m'])
w_tr_left = np.array(track['w_tr_left_m'])

# --- Plot the track centerline and boundaries as a closed polygon ---
dx = np.gradient(x)
dy = np.gradient(y)
length = np.sqrt(dx**2 + dy**2)
tx = dx / length
ty = dy / length
nx = -ty
ny = tx

right_x = x + nx * w_tr_right
right_y = y + ny * w_tr_right
left_x = x - nx * w_tr_left
left_y = y - ny * w_tr_left

# Merge right and left boundaries to form a closed polygon
outline_x = np.concatenate([right_x, left_x[::-1], [right_x[0]]])
outline_y = np.concatenate([right_y, left_y[::-1], [right_y[0]]])

plt.figure(figsize=(10, 8))
plt.plot(x, y, label='Centerline', color='black', linewidth=1)
plt.plot(outline_x, outline_y, label='Track Outline', color='blue', linewidth=2)
plt.fill(outline_x, outline_y, color='lightblue', alpha=0.4, label='Track Area')
plt.xlabel('x (meters)')
plt.ylabel('y (meters)')
plt.title('Suzuka Track with Full Boundaries')
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()

# --- Define two cars ---
cars = [
    {
        'name': 'Mazda RX-8',
        'mass': 1440,
        'max_lateral_g': 0.92,
        'max_accel': 4.0,
        'max_brake': 9.0,
        'top_speed': 230
    },
    {
        'name': 'Lightweight Sports Car',
        'mass': 1200,
        'max_lateral_g': 1.2,
        'max_accel': 5.5,
        'max_brake': 10.5,
        'top_speed': 210
    }
]
g = 9.81

# --- Function to compute speed profile ---
def compute_speed_profile(x, y, car):
    x = np.array(x)
    y = np.array(y)
    dx = np.gradient(x)
    dy = np.gradient(y)
    ddx = np.gradient(dx)
    ddy = np.gradient(dy)
    curvature = np.abs(dx * ddy - dy * ddx) / (dx**2 + dy**2)**1.5
    curvature[curvature < 1e-6] = 1e-6

    max_lateral_a = car['max_lateral_g'] * g
    car_top_speed = car['top_speed'] * 1000 / 3600  # m/s
    v_max_grip = np.sqrt(max_lateral_a / curvature)
    v_max = np.minimum(v_max_grip, car_top_speed)

    v_profile = np.zeros_like(v_max)
    v_profile[0] = v_max[0]
    ds = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
    ds[ds < 1e-6] = 1e-6

    for i in range(1, len(v_profile)):
        v_prev = v_profile[i-1]
        v_possible = np.sqrt(v_prev**2 + 2 * car['max_accel'] * ds[i-1])
        v_profile[i] = min(v_possible, v_max[i])

    v_profile[-1] = v_profile[0]
    for i in range(len(v_profile)-2, -1, -1):
        v_next = v_profile[i+1]
        v_possible = np.sqrt(max(0, v_next**2 + 2 * (-car['max_brake']) * ds[i]))
        v_profile[i] = min(v_profile[i], v_possible)
    return v_profile

# --- Plot speed profiles and print lap times ---
plt.figure(figsize=(12, 8))
for car in cars:
    v_profile = compute_speed_profile(x, y, car)
    ds = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
    ds[ds < 1e-6] = 1e-6
    valid = v_profile[1:] > 1e-3
    if not np.all(valid):
        print(f"Warning: {car['name']} has zero-speed segments. Lap time may be inaccurate.")
    lap_time = np.sum(ds[valid] / v_profile[1:][valid])
    print(f"{car['name']}: Lap time = {lap_time:.2f} s")
    plt.plot(v_profile, label=car['name'])
plt.xlabel('Track Point Index')
plt.ylabel('Speed (m/s)')
plt.title('Speed Profiles for Different Cars on Suzuka')
plt.legend()
plt.grid(True)
plt.show() 