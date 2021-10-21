import os.path
import pickle
from tkinter import *
from tkinter import messagebox

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from scipy.interpolate import interp1d

days_counter = []
mood_list = []
mood_options = ["awful", "bad", "meh", "good", "amazing"]

root = Tk()
root.geometry("750x450")
root.title("Moodcast")


def register_mood(current_mood):
    global mood_list
    global days_counter

    # Put selected mood in list
    mood_score = mood_options.index(current_mood) + 1
    mood_list.append(mood_score)

    # Increase days counter
    days_counter.append(len(days_counter) + 1)

    # Save input
    save_progress()


def show_graph():
    global mood_list
    global days_counter

    # Display graph
    if len(mood_list) > 3:
        make_graph(days_counter, mood_list)
    else:
        messagebox.showwarning(title="Warning", message="First input mood")


def make_graph(days, moods):
    graph_screen = Tk()
    graph_screen.title("Mood progress")

    # Compile lists into array
    x = np.array(days)
    y = np.array(moods)

    # Use cubic interpolation model for smoothing the graph
    cubic_interpolation_model = interp1d(x, y, kind="cubic")
    x_smooth = np.linspace(x.min(), x.max(), 150)
    y_smooth = cubic_interpolation_model(x_smooth)

    # Plot data
    fig = Figure(figsize=(5, 5), dpi=120)
    ax = fig.add_subplot(111)

    # Round x-axis values
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Color bands on y-axis
    ax.axhspan(0, 1, alpha=0.35, color="red")
    ax.axhspan(1, 2, alpha=0.35, color="orange")
    ax.axhspan(2, 3, alpha=0.35, color="yellow")
    ax.axhspan(3, 4, alpha=0.35, color="lightgreen")
    ax.axhspan(4, 5, alpha=0.35, color="limegreen")

    # Set labels and title
    ax.set_ylim([0, 5])
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.set_yticklabels(("", "awful", "bad", "meh", "good", "amazing"), fontsize=9)
    ax.title.set_text("My progress")
    ax.set_xlabel("Days")
    ax.set_ylabel("Mood")

    # Plot graph
    ax.plot(x_smooth, y_smooth, color='yellow', linewidth=3, solid_capstyle='round')

    # Draw graph to the screen
    canvas = FigureCanvasTkAgg(fig, master=graph_screen)
    canvas.draw()
    canvas.get_tk_widget().pack()

    graph_screen.mainloop()


def save_progress():
    # Save data in pickle files in directory
    with open('mood_data.pkl', 'wb') as f:
        pickle.dump(mood_list, f)

    with open('days_data.pkl', 'wb') as f:
        pickle.dump(days_counter, f)


def load_progress():
    global mood_list
    global days_counter

    # Load data from pickle files
    with open('mood_data.pkl', 'rb') as f:
        mood_list = pickle.load(f)

    with open('days_data.pkl', 'rb') as f:
        days_counter = pickle.load(f)


# On startup, load available data
if os.path.exists("./days_data.pkl") and os.path.exists("./mood_data.pkl"):
    load_progress()

# Iterate over mood options and place buttons
for count, mood in enumerate(mood_options):
    mood_btn = Button(root, text=mood.capitalize(), command=lambda mood=mood: register_mood(mood)) \
        .place(relx=(count + 1) * 0.15, rely=0.5)

graph_btn = Button(root, text="Show graph", command=show_graph).place(relx=0.45, rely=0.1)

root.mainloop()
