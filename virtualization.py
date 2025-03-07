import numpy as np
import matplotlib.pyplot as plt

# Generate data points
alpha = np.linspace(0, 2 * np.pi, 100)  # Range of alpha values
sin_squared = np.sin(alpha)**2
cos_formula = (1 - np.cos(2 * alpha)) / 2

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(alpha, sin_squared, label='sin^2(alpha)', linewidth=2)
plt.plot(alpha, cos_formula, label='(1 - cos(2*alpha)) / 2', linestyle='--', linewidth=2)

# Add labels and title
plt.xlabel('Alpha (radians)')
plt.ylabel('Value')
plt.title('Visualization of sin^2(alpha) = (1 - cos(2*alpha)) / 2')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()