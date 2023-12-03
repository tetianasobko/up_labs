import tkinter as tk

WIN_H = 500
WIN_W = 1000
PANEL_H = WIN_H
PANEL_W = 450
CANVAS_H = WIN_H
CANVAS_W = WIN_W - PANEL_W

win = tk.Tk()
win.title("Аналіз чутливості")
win.config(width=WIN_W, height=WIN_H)
win.resizable(False, False)

panel = tk.Frame(win, width=PANEL_W, height=PANEL_H, bd=4, relief=tk.GROOVE)
panel.place(x=0, y=0, width=PANEL_W, height=PANEL_H)

canvas = tk.Canvas(win, width=CANVAS_W, height=CANVAS_H, bg="white")
canvas.place(x=PANEL_W, y=0, width=CANVAS_W, height=CANVAS_W)

def validate_numeric_input(action, value_if_allowed):
    if action == '1':  # insert
        if value_if_allowed and value_if_allowed.strip():
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    else:
        return True

def draw_axes(y_top):
    y_top += 1

    dx = CANVAS_W
    dy = CANVAS_H / (y_top - -1)
    # центр координат
    cx = dy  # перетворюємо координати полотна в координати нашої системи
    cy = y_top * dy
    # створюємо осі
    canvas.create_line(cx, cy, CANVAS_W - cx, cy)
    canvas.create_line(cx, 0, cx, CANVAS_H - dy)
    canvas.create_line(CANVAS_W - cx, 0, CANVAS_W - cx, CANVAS_H - dy)

    # поділки осі Х
    canvas.create_text(dy, cy + 12, text=str(0), font="Verdana 9")
    canvas.create_text(CANVAS_W - dy, cy + 12, text=str(1), font="Verdana 9")

    # поділки осі Y
    y = y_top - 1
    while y > -1:
        if y == 0:
            y -= 1
            continue
        y_canvas = (y - y_top) * dy
        canvas.create_line(cx - 3, -y_canvas, cx + 3, -y_canvas)
        canvas.create_text(cx - 25, -y_canvas, text=str(y), font="Verdana 9")
        y -= 1

    y = y_top - 1
    while y > -1:
        if y == 0:
            y -= 1
            continue
        y_canvas = (y - y_top) * dy
        canvas.create_line(CANVAS_W - dy - 3, -y_canvas, CANVAS_W - dy + 3, -y_canvas)
        canvas.create_text(CANVAS_W - dy + 25, -y_canvas, text=str(y), font="Verdana 9")
        y -= 1
    return dx, dy

def draw_line(y_start, y_end, max_val, color):
    max_val += 1
    cx = dy

    canvas.create_line(cx, (max_val - y_start) * dy, CANVAS_W - cx, (max_val - y_end) * dy, fill=color, width = 2)

def redraw():
    global dx, dy
    # Get values from input fields
    values = [float(entry.get()) for entry in entries]

    # Calculate min and max values
    min_val = min(values)
    max_val = max(values)

    # Clear previous lines and axes on canvas
    canvas.delete("all")

    # Draw axes with min and max values from input fields
    dx, dy = draw_axes(max_val)

    # Draw lines on canvas based on the calculated values
    draw_line(values[0], values[1], max_val, "red")
    
    draw_line(values[2], values[3], max_val, "green")
    
    draw_line(values[4], values[5], max_val, "blue")

    # Convert input values to variables for convenience
    A0, A1, B0, B1, C0, C1 = values[0], values[1], values[2], values[3], values[4], values[5]

    intersections = [
        intersection(A0, A1, B0, B1),
        intersection(C0, C1, B0, B1),
        intersection(A0, A1, C0, C1)
    ]

    intersections = [i for i in intersections if i > 0 and i < 1]
    intersections.extend([0, 1])
    intersections.sort()

    result_label.config(text="")

    for i in range(len(intersections) - 1):
        middle = (intersections[i] + intersections[i + 1]) / 2.0
        best = get_best(A0, A1, B0, B1, C0, C1, middle)
        worst = get_worst(A0, A1, B0, B1, C0, C1, middle)

        result_label.config(text=result_label.cget("text") + f"Для {intersections[i]:.2f} < P(2) < {intersections[i + 1]:.2f}:\n")
        result_label.config(text=result_label.cget("text") + f"Найкраща опція: {best}\n")
        result_label.config(text=result_label.cget("text") + f"Найгірша опція: {worst}\n\n")

def get_best(A0, A1, B0, B1, C0, C1, point):
    a = A0 + (A1 - A0) * point
    b = B0 + (B1 - B0) * point
    c = C0 + (C1 - C0) * point

    if a > b and a > c:
        return "A"
    if b > c:
        return "B"
    return "C"

def get_worst(A0, A1, B0, B1, C0, C1, point):
    a = A0 + (A1 - A0) * point
    b = B0 + (B1 - B0) * point
    c = C0 + (C1 - C0) * point

    if a < b and a < c:
        return "A"
    if b < c:
        return "B"
    return "C"

def intersection(a, b, c, d):
    if c - a == d - b:
        return -1
    return (c - a) / (b - a - d + c)

labels = ['A for Loss:', 'A for Win:', 'B for Loss:', 'B for Win:', 'C for Loss:', 'C for Win:']
table_values = [1, 14, 2, 10, 4, 6]
entries = []
row = 0 
column = 0

for i, label_text in enumerate(labels):
    bg_color = "red" if 'A' in label_text else "green" if 'B' in label_text else "blue"
    label = tk.Label(panel, text=label_text, bg=bg_color)
    label.grid(row = row, column = column, padx=5, pady=15)

    column += 1

    vcmd = panel.register(validate_numeric_input)
    entry = tk.Entry(panel, validate="key", validatecommand=(vcmd, '%d', '%P'))
    entry.grid(row = row, column = column, padx=5, pady=5)
    entries.append(entry)
    
    column += 1
    if column % 4 == 0:
        row += 1
    column %= 4

    entry.insert(tk.END, str(table_values[i]))

but1 = tk.Button(panel, text="Розрахувати", command=redraw)
but1.grid(row=7, columnspan=4, padx=5, pady=30)
result_label = tk.Label(panel, text="", wraplength=300, justify=tk.LEFT)
result_label.grid(row=len(labels) + 3, columnspan=2, padx=5, pady=5)

dx = 1
dy = 1

win.mainloop()
