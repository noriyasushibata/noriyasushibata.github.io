import math
import time
import os

def main():
    width = 80
    height = 24
    radius = 10
    angle = 0
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(height):
            for x in range(width):
                # Center the globe
                cx = x - width // 2
                cy = y - height // 2
                # Calculate distance from center
                dist = math.sqrt(cx**2 + cy**2)
                if dist < radius:
                    # Calculate z for 3D effect
                    z = math.sqrt(radius**2 - dist**2)
                    # Rotate around y-axis
                    x_rot = cx * math.cos(angle) - z * math.sin(angle)
                    z_rot = cx * math.sin(angle) + z * math.cos(angle)
                    # Shade based on z_rot (depth)
                    shade = int((z_rot + radius) / (2 * radius) * 9)
                    # Add color using ANSI escape codes
                    color = 30 + shade  # 30-39 for colors
                    print(f"\033[{color}m{shade}\033[0m", end='')
                else:
                    print(' ', end='')
            print()
        angle += 0.1
        time.sleep(0.1)

if __name__ == "__main__":
    main()