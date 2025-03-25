import pygame
import serial
import time

# Initialize Pygame
pygame.init()

# Set up Pygame screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Distance Graph')

# Set up font for displaying text
font = pygame.font.SysFont(None, 36)

# Serial communication setup
com_port = 'COM26'  # Replace with your correct COM port
baud_rate = 9600
ser = serial.Serial(com_port, baud_rate, timeout=1)
time.sleep(2)  # Wait for the serial port to initialize

# Graph settings
graph_width = screen_width - 50
graph_height = screen_height - 100
line_color = (255, 0, 0)  # Red color for the graph line
bg_color = (0, 0, 0)  # Black background
line_width = 5  # Thicker line
distance_values = []  # List to store distance data

# Function to draw the graph
def draw_graph():
    # Clear the screen
    screen.fill(bg_color)

    # Draw the graph frame
    pygame.draw.rect(screen, (255, 255, 255), (25, 50, graph_width, graph_height), 2)

    # Draw the graph line
    if len(distance_values) > 1:
        for i in range(1, len(distance_values)):
            # Scale the distance to fit within the graph height
            y1 = 50 + (graph_height - (distance_values[i-1] / 70) * graph_height)
            y2 = 50 + (graph_height - (distance_values[i] / 70) * graph_height)
            pygame.draw.line(screen, line_color, 
                             (25 + (i-1) * (graph_width / 70), y1),
                             (25 + i * (graph_width / 70), y2),
                             line_width)

    # Display the distance as text
    if len(distance_values) > 0:
        current_distance = distance_values[-1]
        distance_text = font.render(f'Distance: {current_distance} cm', True, (255, 255, 255))
        screen.blit(distance_text, (25, 10))

    pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read data from the serial port
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()  # Read the line and remove any trailing whitespace
        try:
            distance = float(line)  # Convert the line to a float (assumes the input is a valid number)
            if 0 <= distance <= 70:  # Ensure the distance is within the valid range (0-70 cm)
                distance_values.append(distance)

                # If the graph reaches the end (70 values), reset the graph
                if len(distance_values) > 70:
                    distance_values = distance_values[1:]

        except ValueError:
            pass  # Ignore invalid data

    # Draw the graph and update the screen
    draw_graph()

    # Pause for a short moment to avoid high CPU usage
    pygame.time.wait(100)

# Close the serial connection and Pygame
ser.close()
pygame.quit()
