from tkinter import *
from tkinter import messagebox
from scipy.interpolate import interp1d
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

days_counter = []
mood_list = []
mood_options = ["awful", "bad", "meh", "good", "amazing"]

root = Tk()
root.geometry("750x450")
root.title("Moodcast")


def register_mood(current_mood):
    global updated_days_counter
    global mood_list

    # Put selected mood in list
    mood_score = mood_options.index(current_mood) + 1
    mood_list.append(mood_score)

    # Increase days counter
    days_counter.append(len(days_counter))
    updated_days_counter = [x + 1 for x in days_counter]


def visualize_data():
    # Display graph
    if mood_list:
        make_graph(updated_days_counter, mood_list)
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
    x_smooth = np.linspace(x.min(), x.max(), 500)
    y_smooth = cubic_interpolation_model(x_smooth)

    # Plot data
    fig = Figure(figsize=(5, 5), dpi=100)
    plot = fig.add_subplot(111)
    plot.plot(x_smooth, y_smooth)

    # Draw graph to the screen
    canvas = FigureCanvasTkAgg(fig, master=graph_screen)
    canvas.draw()
    canvas.get_tk_widget().pack()

    graph_screen.mainloop()

# Iterate over mood options and place buttons
for count, mood in enumerate(mood_options):
    mood_btn = Button(root, text=mood.capitalize(), command=lambda mood=mood: register_mood(mood)) \
        .place(relx=(count + 1) * 0.15, rely=0.5)

show_graph = Button(root, text="Show graph", command=visualize_data).place(relx=0.45, rely=0.1)

root.mainloop()
