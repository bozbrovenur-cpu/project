from functools import partial
import tkinter as tk

window_name_FOUR = "Calc"

button_height_FOUR = 5
button_width_FOUR = 10

window_size_FOUR = "800x700"
window_background_color_FOUR = "black"

style_letters_input_FOUR = "Consolas"
size_letters_input_FOUR = 20
s_letters_input_FOUR = "bold"
color_letters_FOUR = "yellow"
color_background_input_FOUR = "green"

max_value_FOUR = 10

root = tk.Tk()
root.title(window_name_FOUR)
root.geometry(window_size_FOUR)
root.configure(bg=window_background_color_FOUR)


disp_var = tk.StringVar(value="0")


def validate_func(*_):
    xFOUR = len(disp_var.get())
    if xFOUR > max_value_FOUR:
        return False
    return True


disp = tk.Entry(
    textvariable=disp_var,
    validate="key",
    # validatecommand=(root.register(validate_func), "%P"),
    font=(style_letters_input_FOUR, size_letters_input_FOUR, s_letters_input_FOUR),
    bg=color_background_input_FOUR,
    fg=color_letters_FOUR,
    justify="right",
    relief="raised",
    insertbackground="red"
)
disp.grid(row=0, column=0, columnspan=3, padx=5, pady=5, ipady=4)


message_disp = tk.Label(root, text="239487293", fg="red",
                        bg="black", font=("Consolas", 20, "bold"))
message_disp.grid(row=5, column=0, columnspan=3, padx=5, pady=5, ipady=4)

busy_flag = False


def print_message(text):
    message_disp.config(text=text)


def entry_control(*_):
    global busy_flag
    if busy_flag:
        return
    busy_flag = True
    entry_string = disp.get()
    if entry_string == None:
        return

    if entry_string == "":
        disp.insert(tk.END, "0")
        entry_string = disp.get()

    if not entry_string.isdigit():
        entry_string = "".join(c for c in entry_string if c.isdigit())
        disp_var.set(entry_string)
    #   23423 000
    if len(entry_string) > 1 and entry_string[0] == "0":
        entry_string = entry_string = entry_string.lstrip("0") or "0"
        disp_var.set(entry_string)
    """
    "".join(c for c in entry_string if c[0] != '0')
        entry_string = entry_string.lstrip("0") or "0"
        disp.delete(0, tk.END)
        disp.insert(tk.END, entry_string)
    entry_string = str(int(entry_string))
    disp.delete(0, tk.END)
    disp.insert(tk.END, entry_string)
    """
    if len(entry_string) > 10:
        disp_var.set(entry_string[:10])
        print_message("Max digits: 10")
    else:
        print_message("Calculator")
    busy_flag = False


disp_var.trace_add("write", entry_control)
buttons = []


def create_btn(rowFOUR, columnFOUR, **kwargs):
    btnFOUR = tk.Button(root, height=button_height_FOUR,
                        width=button_width_FOUR, **kwargs)
    btnFOUR.grid(row=rowFOUR, column=columnFOUR, padx=5, pady=5)
    buttons.append(btnFOUR)


def highlight_button(buttonFOUR):
    # depends on buttons massive
    """Отвечает только за анимацию цифровых, и также обслужующих кнопок"""
    # if digit buttons
    if buttonFOUR.isdigit():
        for button in buttons:
            if button.cget("text").isdigit():
                button.config(bg="yellow", fg="black",
                              relief="raised", bd=4)

        current_btnFOUR = next(
            (b for b in buttons if b.cget("text") == buttonFOUR), None)

        if current_btnFOUR:
            current_btnFOUR.config(bg="green", fg="red", relief="sunken", bd=4)

            root.after(700, lambda: current_btnFOUR.config(
                bg="yellow", fg="black", relief="raised", bd=4))
    elif buttonFOUR.isalpha():
        for button in buttons:
            if button.cget("text").isalpha():
                button.config(bg="red", fg="black", relief="raised", bd=4)
        current_button = next(
            (btn for btn in buttons if btn.cget("text") == buttonFOUR), None)
        if current_button:
            current_button.config(bg="green", fg="red", relief="sunken", bd=4)
            root.after(700, lambda: current_button.config(
                bg="red", fg="black", relief="raised", bd=4))
    elif not buttonFOUR.isalnum():
        for button in buttons:
            if not button.cget("text").isalnum():
                button.config(bg="green", fg="black", relief="raised", bd=4)

        current_button = next(
            (button for button in buttons if button.cget("text") == buttonFOUR), None)

        if current_button:
            current_button.config(bg="yellow", relief="sunken", bd=4)
            root.after(700, lambda: current_button.config(
                bg="green", relief="raised", bd=4))


def handle_digit_input(button):
    highlight_button(button)
    if button.isdigit():
        disp.insert(tk.END, button)


def create_buttons():
    # create 1-9
    for iFOUR in range(1, 10):
        create_btn(((iFOUR-1)//3)+1, (iFOUR-1) %
                   3, text=str(iFOUR), bg="yellow", relief="raised", bd=4,
                   command=lambda lFOUR=iFOUR: handle_digit_input(str(lFOUR)))
    create_btn(4, 0, text="0", bg="yellow", relief="raised", bd=4,
               command=lambda: handle_digit_input("0"))

    # creating backspace button: id = 10
    create_btn(4, 1, text="Backspace", bg="red",
               command=lambda: operation_action("Backspace"))
    # creating Clear button: id = 11
    create_btn(4, 2, text="Clear", bg="red",
               command=lambda: operation_action("Clear"))
    # creating * button
    create_btn(1, 3, text="*", bg="green",
               command=lambda: operation_action("*"))
    # creating / button
    create_btn(2, 3, text="/", bg="green",
               command=lambda: operation_action("/"))
    # creating + button
    create_btn(3, 3, text="+", bg="green",
               command=lambda: operation_action("+"))
    # creating * button
    create_btn(4, 3, text="-", bg="green",
               command=lambda: operation_action("-"))
    # creating * button
    create_btn(5, 3, text="=", bg="green",
               command=lambda: operation_action("="))


val1 = 0
val2 = 0
current_operation = None


def operation_action(operFOUR):
    global val1, val2, operation
    """только отвечает за функционал кнопок, не следит за полем ввода, ведущими нулями и т.д!!!"""
    highlight_button(operFOUR)
    if operFOUR == "Clear":
        disp.delete(0, tk.END)
    elif operFOUR == "Backspace":
        entry_len = len(disp_var.get())
        disp.delete((entry_len or 1) - 1, tk.END)
    elif operFOUR in ("*", "-", "+", "/"):
        val1 = int(disp_var.get() or "0")
        disp_var.set("0")
        operation = operFOUR
    elif operFOUR == "=":
        val2 = int(disp_var.get() or "0")
        disp_var.set("0")
        if operation == "+":
            disp_var.set(str(val1 + val2)[:10])
            val1 = val1 + val2
            val2 = 0
        if operation == "*":
            disp_var.set(str(val1 * val2)[:10])
            val1 = val1 * val2
            val2 = 0
        if operation == "/":
            disp_var.set(str(val1 / val2)[:10])
            val1 = val1 / val2
            val2 = 0
        if operation == "-":
            disp_var.set(str(val1 - val2)[:10])
            val1 = val1 - val2
            val2 = 0

    return


create_buttons()
root.mainloop()
