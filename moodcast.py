import os
import os.path
import pickle
from datetime import date
from statistics import mean
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font

import numpy as np
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from scipy.interpolate import interp1d

"""
TO DO 
- option to choose reminder
- display day / week of year
- weekly report
    + average mood
    + bar chart
    +

- link to other users/friends, see (certain) data from them and contact options of person is not well
"""

days_counter = []
mood_list = []
mood_options = ["awful", "bad", "meh", "good", "amazing"]
bg_col = "#1e1e1e"

root = Tk()
root.geometry("750x450")
root.minsize(450, 350)
root.configure(bg=bg_col)
root.iconbitmap('img/moodcast_icon.ico')
root.title("Moodcast")

font = Font(family="Segoe UI", size=10)


def register_mood(current_mood):
    global mood_list
    global days_counter

    # Put selected mood in list
    mood_score = mood_options.index(current_mood) + 1
    mood_list.append(mood_score)

    # Increase days counter
    days_counter.append(len(days_counter) + 1)

    # Update day label
    update_current_day()

    # Save input
    save_progress()

    messagebox.showinfo(title="Success!", message="Today's input is saved!")

    # Ask to see weekly report every 7 days
    if len(mood_list) % 7 == 0:
        answer = messagebox.askyesno(title="Weekly report",
                                     message="That's a week full of moods, would you like to see your weekly report?")
        if answer: weekly_report()


def show_graph():
    global mood_list
    global days_counter

    # Display graph
    if mood_list:
        if len(mood_list) > 3:
            make_graph(days_counter, mood_list)
        else:
            messagebox.showwarning(title="Warning", message="Wait for day 4 to see graph")
    else:
        messagebox.showwarning(title="Warning", message="You have no registered moods yet!")


def make_graph(days, moods):
    graph_screen = Tk()
    graph_screen.title("Mood progress")
    graph_screen.resizable(False, False)

    # Compile lists into array
    x = np.array(days)
    y = np.array(moods)

    # Use cubic interpolation model for smoothing the graph
    cubic_interpolation_model = interp1d(x, y, kind="cubic")
    x_smooth = np.linspace(x.min(), x.max(), 150)
    y_smooth = cubic_interpolation_model(x_smooth)

    # Plot data
    fig = Figure(figsize=(5, 5), dpi=120)
    fig.patch.set_facecolor('lightgrey')
    ax = fig.add_subplot(111)

    # Round x-axis values
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Color bands on y-axis
    ax.axhspan(0, 1, alpha=0.35, color="red")
    ax.axhspan(1, 2, alpha=0.35, color="orange")
    ax.axhspan(2, 3, alpha=0.35, color="yellow")
    ax.axhspan(3, 4, alpha=0.35, color="lightgreen")
    ax.axhspan(4, 5.25, alpha=0.35, color="limegreen")

    # Set labels and title
    ax.set_ylim([0, 5.25])
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.set_yticklabels(("", "Awful", "Bad", "Meh", "Good", "Amazing"), fontsize=8.5)
    ax.title.set_text("My progress")
    ax.set_xlabel("Days")
    ax.set_ylabel("Mood")

    # Plot graph
    z = np.polyfit(x_smooth, y_smooth, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), "r--", alpha=0.25)
    ax.plot(x_smooth, y_smooth, color='yellow', linewidth=3, solid_capstyle='round')

    # Draw graph to the screen
    canvas = FigureCanvasTkAgg(fig, master=graph_screen)
    canvas.draw()
    canvas.get_tk_widget().pack()


def update_current_day():
    # Set current_day label to the correct day
    current_day.set(days_counter[-1] if days_counter else 0)


def make_bar_chart():
    bar_chart_screen = Tk()

    # Get data from last 7 days
    x = days_counter[-7:]
    y = mood_list[-7:]

    fig = Figure(figsize=(7, 5), dpi=120)
    fig.patch.set_facecolor('lightgrey')
    ax = fig.add_subplot(111)
    ax.bar(x, y, color='#5E10BC')

    canvas = FigureCanvasTkAgg(fig, master=bar_chart_screen)
    canvas.draw()
    canvas.get_tk_widget().pack()


def save_progress():
    # Save data in pickle files in directory
    with open('mood_data.pkl', 'wb') as f:
        pickle.dump(mood_list, f)

    with open('days_data.pkl', 'wb') as f:
        pickle.dump(days_counter, f)


def load_progress():
    global mood_list
    global days_counter

    if os.path.exists("./days_data.pkl") and os.path.exists("./mood_data.pkl"):
        # Load data from pickle files
        with open('mood_data.pkl', 'rb') as f:
            mood_list = pickle.load(f)

        with open('days_data.pkl', 'rb') as f:
            days_counter = pickle.load(f)


def clear_history():
    # Get filesize
    mood_data_filesize = os.path.getsize("./mood_data.pkl")
    days_data_filesize = os.path.getsize("./days_data.pkl")

    # Pickle file with empty list is 5 bytes, so check if not empty
    if mood_data_filesize and days_data_filesize > 5:
        answer = messagebox.askokcancel("Warning", "Do you want to delete your mood history?\n\n"
                                                   "All your previous data will be lost.")
        if answer:
            # Empty out pickle files
            with open('mood_data.pkl', 'wb') as f:
                pickle.dump([], f)

            with open('days_data.pkl', 'wb') as f:
                pickle.dump([], f)

            # Reload data
            load_progress()

            # Update day to 0
            update_current_day()
    else:
        messagebox.showwarning(title="Warning", message="You have no mood history yet!")


def show_info():
    messagebox.showinfo(title="How does this work?",
                        message="This program helps you track your mood! \n\n"
                                "Simply click on the emotion that you're feeling right now everyday, "
                                "and you can see your progress displayed in a graph (only visible after day 4).\n"
                                "If you want to erase your previous entries, click on 'Clear history'.\n\n"
                                "Consistency is key, so be sure to let us know how you're feeling "
                                "to keep track of your moods the best!\n\n"
                                "If you are struggling with mental health issues, please visit wannatalkaboutit.com")


def weekly_report():
    weekly_report_screen = Tk()
    weekly_report_screen.title("My weekly report")
    weekly_report_screen.geometry("450x650")
    weekly_report_screen.configure(bg=bg_col)
    weekly_report_screen.iconbitmap('img/moodcast_icon.ico')

    # Get scores from last 7 days and convert to moods
    weekly_scores = mood_list[-7:]
    weekly_moods = [mood_options[score - 1] for score in weekly_scores]

    # Calculate average mood
    avg = mood_options[round((mean(weekly_scores))) - 1]

    # Display average mood
    Label(weekly_report_screen, text=f"Your average mood this week: {avg}", font=('Segoe UI Bold', 15), bg=bg_col,
          fg='white').place(relx=0.5, rely=0.125, anchor=CENTER)

    # Bar chart button
    Button(weekly_report_screen, text="Show this week's progress", command=make_bar_chart,
           font=('Segoe UI Bold', 13), bg='#5E10BC', fg='white', padx=8, pady=8) \
        .place(relx=0.5, rely=0.22, anchor=CENTER)

    # Place days with the appropriate moods
    for count, mood in enumerate(weekly_moods):
        Label(weekly_report_screen, text=f"Day {count + 1}:", font=('Segoe UI Bold', 20), bg=bg_col, fg='white') \
            .place(relx=0.3, rely=(count + 3) * spacing * 0.68, anchor=CENTER)
        Label(weekly_report_screen, text=mood, font=('Segoe UI Bold', 20), bg=bg_col, fg='#5E10BC') \
            .place(relx=0.7, rely=(count + 3) * spacing * 0.68, anchor=CENTER)


spacing = 0.15
img_size = [50, 50]
img_list = []

for count, mood in enumerate(mood_options):
    # Place buttons
    mood_btn = Button(root, text=mood.capitalize(), command=lambda mood=mood: register_mood(mood), width=7, font=font,
                      bg='darkgrey', fg='black') \
        .place(relx=(count + 1) * spacing, rely=0.6)

    # Place images
    mood_img = Image.open(f"img/{mood}.png")
    mood_img_copy = mood_img.resize(img_size, Image.ANTIALIAS)
    mood_img_resized = ImageTk.PhotoImage(mood_img_copy)
    img_list.append(mood_img_resized)
    Label(root, image=mood_img_resized, bg=bg_col).place(relx=(count + 1) * spacing, rely=0.45)

# On startup, load available data
load_progress()

# Get days registered
current_day = StringVar()
update_current_day()

# Tkinter elements
graph_btn = Button(root, text="Show progress", command=show_graph, font=font, bg='#5E10BC', fg='white', padx=8, pady=8) \
    .place(relx=0.5, rely=0.8, anchor=CENTER)
banner_lbl = Label(root, text="Moodcast", font=('Segoe UI Bold', 32), bg='#5E10BC', fg='white') \
    .pack(fill=X, anchor='center')
date_lbl = Label(root, text=str(date.today().strftime("%B %d, %Y")), font=('Segoe UI Bold', 18), bg=bg_col,
                 fg='darkgrey').pack(anchor='center')
day_lbl = Label(root, textvariable=current_day, font=('Segoe UI Bold', 18), bg=bg_col,
                fg='darkgrey').pack(anchor='center')
text_lbl = Label(root, text="How are you feeling today?", font=('Segie UI Bold', 26), bg=bg_col, fg='white').place(
    relx=0.5, rely=0.35, anchor=CENTER)
clear_btn = Button(root, text="Clear history", command=clear_history, font=font, bg='darkgrey', fg='black').place(
    rely=1, relx=1, x=-7, y=-7, anchor=SE)
info_btn = Button(root, text="?", command=show_info, font=font, bg='darkgrey', fg='black', width=3).place(
    rely=1, relx=0, x=7, y=-7, anchor=SW)

root.mainloop()
