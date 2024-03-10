import tkinter as tk
from tkinter import messagebox, IntVar,Toplevel
import time

room_dict = {
    'A': (1, 1), 'B': (1, 2), 'C': (1, 3),
    'D': (2, 1), 'E': (2, 2), 'F': (2, 3),
    'G': (3, 1), 'H': (3, 2), 'I': (3, 3)
}

connections = {
    'A': ['B', 'D'],
    'B': ['A', 'C', 'E'],
    'C': ['B', 'F'],
    'D': ['A', 'E', 'G'],
    'E': ['B', 'D', 'F', 'H'],
    'F': ['C', 'E', 'I'],
    'G': ['D', 'H'],
    'H': ['E', 'G', 'I'],
    'I': ['F', 'H']
}
fringe_steps = []

room_coordinates = {'A': (50, 50), 'B': (150, 50), 'C': (250, 50),
                    'D': (50, 150), 'E': (150, 150), 'F': (250, 150),
                    'G': (50, 250), 'H': (150, 250), 'I': (250, 250)}

def draw_wall(room1, room2):
    x1, y1 = room_coordinates[room1]
    x2, y2 = room_coordinates[room2]
    canvas.create_line(x1, y1, x2, y2, fill='red', width=2)

def highlight_final_path_with_delay(final_path, delay=1000):
    highlighted_labels = []

    for room in final_path:
        label = room_labels[room]
        highlighted_labels.append(label)
        label.config(bg='yellow')
        root.update_idletasks()
        time.sleep(delay / 1000)


    for label in highlighted_labels:
        label.config(bg='SystemButtonFace')

def display_result_step_by_step(result_steps, final_path, fringe_steps, final_cost):
    steps_display.config(state=tk.NORMAL)
    steps_display.insert(tk.END, "Algorithm Steps:\n")
    for step, fringe in zip(result_steps, fringe_steps):
        steps_display.insert(tk.END, f"Step: {step}\nFringe: {fringe}\nExpanded Node: {result_steps}\n")
    steps_display.insert(tk.END, f"Final Path: {final_path}\nFinal Cost: {final_cost}\n\n")
    steps_display.config(state=tk.DISABLED)

def start_game():
    initial_state = initial_state_entry.get().upper()
    goal_state = goal_state_entry.get().upper()
    search_type = search_type_var.get().upper()

    if initial_state not in room_dict:
        messagebox.showerror("Error", "Invalid initial state. Please enter a valid letter (A-I).")
    elif goal_state not in room_dict:
        messagebox.showerror("Error", "Invalid goal state. Please enter a valid letter (A-I).")
    else:
        if search_type == 'UCS':
            uniform_cost_search(initial_state, goal_state, room_dict, search_type)
        elif search_type == 'A*':
            a_star_search(initial_state, goal_state, room_dict, search_type)
        else:
            messagebox.showerror("Error", "Invalid search type. Please enter 'UCS' or 'A*'.")

def update_steps_display(step_text):
    steps_display.config(state=tk.NORMAL)
    steps_display.insert(tk.END, step_text + '\n')
    steps_display.config(state=tk.DISABLED)

def uniform_cost_search(initial_state, goal_state, room_dict, search_type):
    counter = 0
    expanded_nodes = []
    fringe = [[0, initial_state]]
    path = []
    current = initial_state
    a = True
    while a:
        counter += 1

        fringe.sort()
        step_text = f"Step {counter}: Fringe - {fringe}\nExpanded Node: {fringe[0][1][-1]}"
        update_steps_display(step_text)

        cost = fringe[0][0]
        current = fringe[0][1]
        expanded_nodes.append(current[-1])
        fringe_steps.append(str(fringe))

        if current[-1] == goal_state:
            path = current
            step_text = f"Path: {path}\nCost: {cost}"
            update_steps_display(step_text)
            highlight_final_path_with_delay(path)
            a = False
            break

        fringe.pop(0)

        for i in connections[current[-1]]:
            if i not in expanded_nodes:
                new_cost = cost

                if search_type == 'UCS':
                    if room_dict[current[-1]][0] == room_dict[i][0]:
                        new_cost += 2
                    elif room_dict[current[-1]][1] == room_dict[i][1]:
                        new_cost += 1

                fringe.append([new_cost, current + i])

        if counter == 10:
            messagebox.showinfo("Goal Not Reached", "Goal can't be reached! You reached the 10th node.")
            step_text = f"Path: {path}\nCost: {cost}"
            update_steps_display(step_text)
            a = False
            break

def a_star_search(initial_state, goal_state, room_dict, search_type):
    counter = 0
    expanded_nodes = []
    fringe = [[manhattan_distance(initial_state, goal_state), initial_state]]
    path = []
    current = initial_state
    a = True
    while a:
        counter += 1

        fringe.sort()
        step_text = f"Step {counter}: Fringe - {fringe}\nExpanded Node: {fringe[0][1][-1]}"
        update_steps_display(step_text)
        print(fringe)

        cost = fringe[0][0]
        current = fringe[0][1]
        print("Expanded Node:", current[-1])
        expanded_nodes.append(current[-1])
        fringe_steps.append(str(fringe))

        if current[-1] == goal_state:
            path = current
            step_text = f"Path: {path}\nCost: {cost}"
            update_steps_display(step_text)
            highlight_final_path_with_delay(path)
            print(path)
            a = False

        fringe.pop(0)

        for i in connections[current[-1]]:
            if i not in expanded_nodes:
                new_cost = cost - manhattan_distance(current[-1], goal_state)

                if search_type == 'A*':
                    if room_dict[current[-1]][0] == room_dict[i][0]:
                        new_cost = new_cost + 2 + manhattan_distance(i, goal_state)
                    elif room_dict[current[-1]][1] == room_dict[i][1]:
                        new_cost = new_cost + 1 + manhattan_distance(i, goal_state)

                fringe.append([new_cost, current + i])
                new_cost = new_cost - manhattan_distance(i, goal_state)

        if counter == 10:
            print("Goal not reached!")
            step_text = f"Path: {path}\nCost: {cost}"
            update_steps_display(step_text)
            a = False

def manhattan_distance(i, goal_state):
    return abs(room_dict[i][0] - room_dict[goal_state][0]) + abs(room_dict[i][1] - room_dict[goal_state][1])

def define_walls(var):
    walls_dict = {
        'AB': v1, 'AD': v2, 'BC': v3,
        'BE': v4, 'CF': v5, 'DE': v6,
        'DG': v7, 'EF': v8, 'EH': v9,
        'GH': v10, 'HI': v11, 'FI': v12
    }

    walls = [key for key, value in walls_dict.items() if value.get() == 1]

    for wall in walls:
        room1, room2 = wall[0], wall[1]
        if room1 in connections and room2 in connections[room1]:
            connections[room1].remove(room2)
            connections[room2].remove(room1)

    return connections

root = tk.Tk()
root.title("Search Game")

main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0)

box_frame = tk.Frame(root)
box_frame.grid(row=2, column=1, padx=30, pady=30)

canvas = tk.Canvas(box_frame, width=300, height=300)
canvas.grid(row=0, column=0)

baslik = tk.Label(root, text="Search Game", font=('Arial', 16))
baslik.grid(row=1, column=1, pady=40)

initial_state_label = tk.Label(root, text="Initial State:", font=('Arial', 12))
initial_state_label.grid(row=3, column=0, padx=10, pady=10)
initial_state_entry = tk.Entry(root, width=5)
initial_state_entry.grid(row=3, column=1, padx=10, pady=10)

goal_state_label = tk.Label(root, text="Goal State:", font=('Arial', 12))
goal_state_label.grid(row=4, column=0, padx=10, pady=10)
goal_state_entry = tk.Entry(root, width=5)
goal_state_entry.grid(row=4, column=1, padx=10, pady=10)

search_type_label = tk.Label(root, text="Search Type:", font=('Arial', 12))
search_type_label.grid(row=5, column=0, padx=10, pady=10)

search_type_var = tk.StringVar(root)
search_type_var.set("UCS")  # Default value

search_type_dropdown = tk.OptionMenu(root, search_type_var, "UCS", "A*")
search_type_dropdown.grid(row=5, column=1, padx=10, pady=10)

define_walls_label = tk.Label(root, text="Define Walls", font=('Arial', 12))
define_walls_label.grid(row=6, column=0, padx=10, pady=10)

walls_frame = tk.Frame(root)
walls_frame.grid(row=6, column=1, padx=10, pady=10)

v1 = tk.IntVar()
wall1_check = tk.Checkbutton(walls_frame, text="AB", variable=v1, command=lambda: define_walls(v1))
wall1_check.grid(row=0, column=0, padx=10, pady=10)
v2 = tk.IntVar()
wall2_check = tk.Checkbutton(walls_frame, text="AD", variable=v2, command=lambda: define_walls(v2))
wall2_check.grid(row=0, column=1, padx=10, pady=10)
v3 = tk.IntVar()
wall3_check = tk.Checkbutton(walls_frame, text="BC", variable=v3, command=lambda: define_walls(v3))
wall3_check.grid(row=0, column=2, padx=10, pady=10)
v4 = tk.IntVar()
wall4_check = tk.Checkbutton(walls_frame, text="BE", variable=v4, command=lambda: define_walls(v4))
wall4_check.grid(row=1, column=0, padx=10, pady=10)
v5 = tk.IntVar()
wall5_check = tk.Checkbutton(walls_frame, text="CF", variable=v5, command=lambda: define_walls(v5))
wall5_check.grid(row=1, column=1, padx=10, pady=10)
v6 = tk.IntVar()
wall6_check = tk.Checkbutton(walls_frame, text="DE", variable=v6, command=lambda: define_walls(v6))
wall6_check.grid(row=1, column=2, padx=10, pady=10)
v7 = tk.IntVar()
wall7_check = tk.Checkbutton(walls_frame, text="DG", variable=v7, command=lambda: define_walls(v7))
wall7_check.grid(row=2, column=0, padx=10, pady=10)
v8 = tk.IntVar()
wall8_check = tk.Checkbutton(walls_frame, text="EF", variable=v8, command=lambda: define_walls(v8))
wall8_check.grid(row=2, column=1, padx=10, pady=10)
v9 = tk.IntVar()
wall9_check = tk.Checkbutton(walls_frame, text="EH", variable=v9, command=lambda: define_walls(v9))
wall9_check.grid(row=2, column=2, padx=10, pady=10)
v10 = tk.IntVar()
wall10_check = tk.Checkbutton(walls_frame, text="GH", variable=v10, command=lambda: define_walls(v10))
wall10_check.grid(row=3, column=0, padx=10, pady=10)
v11 = tk.IntVar()
wall11_check = tk.Checkbutton(walls_frame, text="HI", variable=v11, command=lambda: define_walls(v11))
wall11_check.grid(row=3, column=1, padx=10, pady=10)
v12 = tk.IntVar()
wall12_check = tk.Checkbutton(walls_frame, text="FI", variable=v12, command=lambda: define_walls(v12))
wall12_check.grid(row=3, column=2, padx=10, pady=10)

start_button = tk.Button(root, text="Start", font=('Arial', 12), command=start_game)
start_button.grid(row=7, column=1, padx=10, pady=10)

box_frame = tk.Frame(root)
box_frame.grid(row=2, column=1, padx=30, pady=30)

label1 = tk.Label(box_frame, text='A', font=('Arial', 24), width=5, height=2, relief='ridge')
label1.grid(row=0, column=0)

label2 = tk.Label(box_frame, text='B', font=('Arial', 24), width=5, height=2, relief='ridge')
label2.grid(row=0, column=1)

label3 = tk.Label(box_frame, text='C', font=('Arial', 24), width=5, height=2, relief='ridge')
label3.grid(row=0, column=2)

label4 = tk.Label(box_frame, text='D', font=('Arial', 24), width=5, height=2, relief='ridge')
label4.grid(row=1, column=0)

label5 = tk.Label(box_frame, text='E', font=('Arial', 24), width=5, height=2, relief='ridge')
label5.grid(row=1, column=1)

label6 = tk.Label(box_frame, text='F', font=('Arial', 24), width=5, height=2, relief='ridge')
label6.grid(row=1, column=2)

label7 = tk.Label(box_frame, text='G', font=('Arial', 24), width=5, height=2, relief='ridge')
label7.grid(row=2, column=0)

label8 = tk.Label(box_frame, text='H', font=('Arial', 24), width=5, height=2, relief='ridge')
label8.grid(row=2, column=1)

label9 = tk.Label(box_frame, text='I', font=('Arial', 24), width=5, height=2, relief='ridge')
label9.grid(row=2, column=2)

steps_display = tk.Text(root, height=10, width=100)
steps_display.grid(row=1, column=2, rowspan=7, padx=10, pady=10, sticky="nsew")
steps_display.insert(tk.END, "Algorithm Steps:\n")
steps_display.config(state=tk.DISABLED)

label1 = tk.Label(box_frame, text='A', font=('Arial', 24), width=5, height=2, relief='ridge')

room_labels = {'A': label1, 'B': label2, 'C': label3, 'D': label4, 'E': label5, 'F': label6, 'G': label7, 'H': label8, 'I': label9}
label1.grid(row=0, column=0)

root.mainloop()