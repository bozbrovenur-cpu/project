import tkinter as tk
from functools import partial
root = tk.Tk()
root.title("Цифровая панель")
root.geometry("800x700")

# GLOBAL VARS
disp_var = tk.StringVar(value="0")
buttons = []
btn_flag = False
# root.configure(bg="yellow")  # print(2//3)
# exit()


# def validate_input(new_value):
# return new_value == "" or new_value.isdigit()
#    d = 1

def btn_logic(*_):
    global btn_flag
    if btn_flag:
        return
    btn_flag = True
    s = disp_var.get()

    # если не цифра — очищаем
    if not s.isdigit():
        disp.delete(0, tk.END)
        disp.insert(tk.END, "".join(ch for ch in s if ch.isdigit()))

    if s == "":
        disp.delete(0, tk.END)
        disp.insert(tk.END, "0")

    # если больше одного символа и начинается с 0 — убираем нули
    elif len(s) > 1 and s[0] == "0":
        disp.delete(0, tk.END)
        disp.insert(tk.END, s.lstrip("0") or "0")

    _normalizing = False


disp_var.trace_add("write", btn_logic)


def create09():
    # Создаём кнопки 1-9
    for i in range(1, 10):
        btn = tk.Button(root, text=str(i), width=10, height=5,
                        command=lambda n=i: disp.insert(tk.END, str(n)))
    btn.grid(row=(i-1)//3,
             column=(i-1) % 3, padx=5, pady=5)
    buttons.append(btn)  # сохраняем ссылку на объект кнопки


def disable_all():
    for b in buttons:
        b.config(state="disabled")  # отключаем все кнопки


def enable_all():
    for b in buttons:
        b.config(state="normal")    # включаем все кнопки обратно


create09()
# zero button
btn = tk.Button(
    root, text="0", width=10, height=5, command=lambda lFOUR=0: change_value(lFOUR))
btn.grid(row=3, column=0, padx=5, pady=5)
buttons.append(btn)

# C button
btn = tk.Button(root, text="C", bg="red", width=10, height=5,
                command=lambda lFOUR=11: change_value(lFOUR))
btn.grid(row=3, column=1, padx=5, pady=5,)
buttons.append(btn)
disp = tk.Entry(root,
                textvariable=disp_var,
                validate="key",
                # validatecommand=(root.register(validate_input), "%P"),
                font=("Consolas", 20, "bold"),
                bg="yellow",
                fg="blue",
                justify="right",
                relief="raised",
                insertbackground="green")
disp.grid(row=4, column=0, columnspan=3, padx=5, pady=5, ipady=4)
# disp.pack()
root.mainloop()
