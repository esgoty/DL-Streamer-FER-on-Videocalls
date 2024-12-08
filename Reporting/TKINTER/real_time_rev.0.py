import tkinter as tk
import time
from threading import Thread
import json
import math
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')  # Use TkAgg backend for embedding plots in Tkinter



# Emotion mapping function
def emotion_mapping(emotion_label):
    positive_emotions = {'happy', 'surprise'}
    negative_emotions = {'sad', 'angry', 'fear'}
    
    if emotion_label in positive_emotions:
        return 'positive'
    elif emotion_label in negative_emotions:
        return 'negative'
    return 'neutral'

# Load points from the last 10 lines of a JSON file
def load_points_from_json(filename):
    points_dict = {}

    # Open the file and read all lines
    with open(filename, 'r') as f:
        last_10_lines = [line for line in f.readlines() if line.strip()][-10:]

    for line in last_10_lines:
        data = json.loads(line)
        timestamp = data.get("timestamp")
        if timestamp:
            points_dict[timestamp] = [
                [obj["x"], obj["y"], emotion_mapping(obj["emotion"]["label"])]
                for obj in data.get("objects", [])
            ]
    
    return points_dict

# Calculate Euclidean distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Function to check closest object to the window corner
def find_closest_object_to_corner(corner_x, corner_y, points_dict):
    closest_objects = []

    for timestamp, objects in points_dict.items():
        closest_object = None
        min_distance = float('inf')

        # Find the closest object to the corner
        for obj in objects:
            x, y, emotion = obj
            distance = calculate_distance(corner_x, corner_y, x, y)
            if distance < min_distance:
                min_distance = distance
                closest_object = obj

        if closest_object:
            closest_objects.append(closest_object)

    return closest_objects

def count_distinct_values(lst):
    # Extract labels from each element in the list
    labels = [item[2] for item in lst]
    
    # Count occurrences of each distinct label
    value_counts = Counter(labels)
    
    return dict(value_counts)  # Return as a dictionary


# Function to update window and find closest objects
def create_window_and_check(filename):
    window = tk.Tk()
    window.geometry("300x75")
    window.title("Real Time Metrics")

    # Create a canvas for Matplotlib figures
    fig, ax = plt.subplots(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    def update_histogram():
        while True:
            # Get the current position of the window (top-left corner)
            corner_x = window.winfo_x()
            corner_y = window.winfo_y()

            # Load points from the JSON file
            points_dict = load_points_from_json(filename)

            # Find closest objects to the window's top-left corner
            closest_objects = find_closest_object_to_corner(corner_x, corner_y, points_dict)

            # Map emotions and count occurrences
            mapped_emotions_count = count_distinct_values(closest_objects)

            # Clear the previous histogram
            ax.clear()

            # Create a new histogram
            ax.bar(mapped_emotions_count.keys(), mapped_emotions_count.values(), color='skyblue')
            plt.grid(False)  # Remove grid lines
            plt.yticks([])  # Remove y-axis labels
            ax.tick_params(axis="x",direction="in", pad=-25)
            plt.subplots_adjust(bottom=0.1)  # Increase bottom margin by 0.2
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(True)
            ax.spines['left'].set_visible(False)


            # Draw the updated histogram on the Tkinter canvas
            canvas.draw()

            # Wait for 1 second before checking again
            time.sleep(1)

    # Start the background thread to update the histogram
    thread = Thread(target=update_histogram)
    thread.daemon = True
    thread.start()

    # Run the Tkinter main loop
    window.mainloop()

# Example usage
filename = '/home/santi/Documents/TP-FINAL-CEIA/Recursos/VolumenVirtualDLStreamer/thepep.json'  # JSON file to read from
create_window_and_check(filename)