# simulate diff possible racing lines through the corner

# from tight (inner) to wide (outer)
radii = np.linspace(radius - 10, radius + 10, 5)  # 5 lines, 10m inside/outside

# car grip: max lateral acceleration defined by (a = v^2 / r)  "Essentially, the faster the vehicle goes and the tighter the curve (smaller radius), the greater the lateral acceleration."
g = 9.81  # grav
max_lateral_a = car['max_lateral_g'] * g

lap_times = []
for r in radii:
    # const radius corner, max speed = sqrt(a * r)
    max_speed = np.sqrt(max_lateral_a * r)
    # Arc length = angle * radius (for 90 degrees = pi/2 radians)
    arc_length = (np.pi / 2) * r
    # Time = distance / speed
    time = arc_length / max_speed
    lap_times.append(time)
    print(f"Radius: {r:.1f} m | Max speed: {max_speed:.2f} m/s | Time: {time:.2f} s")

# Plot the different lines on the track
plt.figure(figsize=(6,6))
for r in radii:
    x_line = r * np.cos(theta)
    y_line = r * np.sin(theta)
    plt.plot(x_line, y_line, label=f'Radius {r:.1f} m')
plt.xlabel('x (meters)')
plt.ylabel('y (meters)')
plt.title('Possible Racing Lines Through Corner')
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()

# Plot lap time vs. radius
plt.figure()
plt.plot(radii, lap_times, marker='o')
plt.xlabel('Corner Radius (m)')
plt.ylabel('Corner Time (s)')
plt.title('Corner Time vs. Racing Line Radius')
plt.grid(True)
plt.show()