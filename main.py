import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import threading
from stats_service import *
from battery_optimizer import *

cpu_cores_load = []
cpu_load = 0
cpu_cores = get_cpu_cores_number()
cpu_threads = get_cpu_threads_number()
cpu_min_freq = get_cpu_min_freq()
cpu_max_freq = get_cpu_max_freq()
ram_volume = get_ram_volume_mb()
ram_load_MB = 0
ram_load_percent = 0
disk_read_speed = 0
disk_write_speed = 0
gpu_load_percent = 0
gpu_memory_volume = get_gpu_memory_volume_mb()
gpu_memory_load_MB = 0
gpu_memory_load_percent = 0
battery_reserve = 0
battery_status = 0
battery_status_digit = None
battery_time_remaining = 0
battery_reccomended_schema = 0
is_optimization_needed = False


def update_stats():
    threading.Timer(0, update_cpu_cores_load).start()
    threading.Timer(0, update_disk_read_speed).start()
    threading.Timer(0, update_gpu_load_percent).start()
    threading.Timer(1.1, update_cpu_load).start()
    threading.Timer(1.1, update_ram_load).start()
    threading.Timer(1.1, update_disk_write_speed).start()
    threading.Timer(1.1, update_gpu_memory_load).start()
    threading.Timer(1.1, update_battery).start()
    tree.delete(*tree.get_children())
    for i in range(len(cpu_cores_load)):
        tree.insert("",
                    tk.END,
                    values=(f"№{i + 1}",
                            f"{cpu_cores_load[i]:.2f} %"))
    cpu_load_value_label.config(text=f"{cpu_load:.2f} %")
    ram_load_MB_value_label.config(text=f"{ram_load_MB:.1f} МБ")
    ram_load_percent_value_label.config(text=f"{ram_load_percent:.2f} %")
    disk_read_speed_value_label.config(text=f"{disk_read_speed:.1f} МБ/c")
    disk_write_speed_value_label.config(text=f"{disk_write_speed:.1f} МБ/c")
    gpu_load_percent_value_label.config(text=f"{gpu_load_percent:.2f} %")
    gpu_memory_load_MB_value_label.config(text=f"{gpu_memory_load_MB:.1f} МБ")
    gpu_memory_load_percent_value_label.config(text=f"{gpu_memory_load_percent:.2f} %")
    battery_reserve_value_label.config(text=f"{battery_reserve:.0f} %")
    battery_status_value_label.config(text=f"{battery_status}")
    battery_time_remaining_value_label.config(text=f"{battery_time_remaining}")
    root.after(1500, update_stats)


def update_cpu_cores_load():
    global cpu_cores_load
    cpu_cores_load = get_cpu_load_per_core_percent()


def update_cpu_load():
    global cpu_load
    cpu_load = get_cpu_load_summary_percent()


def update_ram_load():
    global ram_load_MB
    global ram_load_percent
    ram_load_MB = get_ram_load_mb()
    ram_load_percent = get_ram_load_percent()


def update_disk_read_speed():
    global disk_read_speed
    disk_read_speed = get_disk_avg_read_speed()


def update_disk_write_speed():
    global disk_write_speed
    disk_write_speed = get_disk_avg_write_speed()


def update_gpu_load_percent():
    global gpu_load_percent
    gpu_load_percent = get_gpu_load_percent()


def update_gpu_memory_load():
    global gpu_memory_load_percent
    global gpu_memory_load_MB
    gpu_memory_load_MB = get_gpu_memory_load_mb()
    gpu_memory_load_percent = get_gpu_memory_load_percent()


def update_battery():
    global battery_reserve
    global battery_status
    global battery_time_remaining
    global battery_status_digit
    battery_reserve = get_battery_reserve_percent()
    if get_battery_status():
        battery_time_remaining = "Информация недоступна (питание от сети)"
        battery_status = "Питание от сети (заряжается)"
        battery_status_digit = 1
    else:
        if get_battery_time_reserve() > 100:
            battery_status = "Разряжается"
            battery_time_remaining = "Получении информации..."
            battery_status_digit = 0
        else:
            battery_status = "Разряжается"
            time_reserve = get_battery_time_reserve()
            hours = int(time_reserve)
            mins = (time_reserve - hours) * 60
            battery_time_remaining = f"{hours:.0f}ч {mins:.0f}мин"
            battery_status_digit = 0


def update_battery_reccomended_schema():
    global battery_status_digit
    global battery_reserve
    global battery_reccomended_schema
    if battery_status_digit == 0 and battery_reserve in range(50, 101):
        battery_reccomended_schema = 2
    elif battery_status_digit == 0 and battery_reserve in range(0, 50):
        battery_reccomended_schema = 1
    elif battery_status_digit == 1:
        battery_reccomended_schema = 3


def diagnostics():
    global battery_reccomended_schema
    global is_optimization_needed
    update_battery_reccomended_schema()
    if battery_reccomended_schema != check_power_scheme():
        is_optimization_needed = True
        messagebox.showwarning("Предупреждение",
                               "Текущая схема энергопотребления не является опитимальной для показателей "
                               "аккумулятора.\n"
                               "Оптимизируйте схему энергопотребления.")
    elif battery_reccomended_schema == 1:
        is_optimization_needed = False
        messagebox.showinfo("Информация",
                            "Текущая схема энергоптребления является оптимальной (Энергосбережение).")
    elif battery_reccomended_schema == 2:
        is_optimization_needed = False
        messagebox.showinfo("Информация",
                            "Текущая схема энергоптребления является оптимальной (Баланс).")
    elif battery_reccomended_schema == 3:
        is_optimization_needed = False
        messagebox.showinfo("Информация",
                            "Текущая схема энергоптребления является оптимальной (Производительность).")

    if is_optimization_needed:
        optimize_button.config(state=tk.NORMAL)


def optimize():
    global battery_reccomended_schema
    global is_optimization_needed
    if battery_reccomended_schema == 1:
        set_power_scheme_power_saver()
        messagebox.showinfo("Информация",
                            "Установлена оптимальная схема энергопотребления (Энергосбережение).")
    elif battery_reccomended_schema == 2:
        set_power_scheme_balanced()
        messagebox.showinfo("Информация",
                            "Установлена оптимальная схема энергопотребления (Баланс).")
    elif battery_reccomended_schema == 3:
        messagebox.showinfo("Информация",
                            "Установлена оптимальная схема энергопотребления (Производительность).")
        set_power_scheme_high_performance()
    is_optimization_needed = False
    optimize_button.config(state=tk.DISABLED)


def unlock_diagnostics_button():
    diagnostics_button.config(state=tk.NORMAL)


root = tk.Tk()
root.title("Оптимизация и диагностика энергопотребления")
big_font = font.Font(family="Arial",
                     size=18)

default_font = font.Font(family="Arial",
                         size=14)

cpu_cores_label = tk.Label(root,
                           text="Загрузка ядер (потоков) процессора:",
                           font=big_font)

tree = ttk.Treeview(root,
                    height=cpu_threads)

tree["columns"] = ("Ядро (поток)", "Загрузка")

tree.column("#0",
            width=0,
            stretch=tk.NO)

tree.column("Ядро (поток)",
            anchor=tk.W,
            width=100)

tree.column("Загрузка",
            anchor=tk.W,
            width=100)

tree.heading("#0",
             text="",
             anchor=tk.W)

tree.heading("Ядро (поток)",
             text="Ядро (поток)",
             anchor=tk.W)

tree.heading("Загрузка",
             text="Загрузка",
             anchor=tk.W)

cpu_load_label = tk.Label(root,
                          text="Загрузка ЦП:",
                          font=default_font,
                          padx=150)

cpu_load_value_label = tk.Label(root,
                                font=default_font,
                                width=70,
                                padx=150)

cpu_cores_count_label = tk.Label(root,
                                 text="Количество физических ядер ЦП:",
                                 font=default_font,
                                 padx=150)

cpu_cores_count_value_label = tk.Label(root,
                                       text=str(cpu_cores),
                                       font=default_font,
                                       width=70,
                                       padx=150)

cpu_threads_label = tk.Label(root,
                             text="Количество виртуальных ядер (потоков) ЦП:",
                             font=default_font,
                             padx=150)

cpu_threads_value_label = tk.Label(root,
                                   text=str(cpu_threads),
                                   font=default_font,
                                   width=70,
                                   padx=150)

cpu_min_freq_label = tk.Label(root,
                              text="Минимальная частота работы процессора:",
                              font=default_font,
                              padx=150)

cpu_min_freq_value_label = tk.Label(root,
                                    text=f"{cpu_min_freq:.0f} МГц",
                                    font=default_font,
                                    width=70,
                                    padx=150)

cpu_max_freq_label = tk.Label(root,
                              text="Максимальная частота работы процессора:",
                              font=default_font,
                              padx=150)

cpu_max_freq_value_label = tk.Label(root,
                                    text=f"{cpu_max_freq:.0f} МГц",
                                    font=default_font,
                                    width=70,
                                    padx=150)

ram_volume_label = tk.Label(root,
                            text="Общий объём оперативной памяти:",
                            font=default_font,
                            padx=150)

ram_volume_value_label = tk.Label(root,
                                  text=f"{ram_volume:.1f} МБ",
                                  font=default_font,
                                  width=70,
                                  padx=150)

ram_load_MB_label = tk.Label(root,
                             text="Объём загруженной оперативной памяти (в МБ):",
                             font=default_font,
                             padx=150)

ram_load_MB_value_label = tk.Label(root,
                                   font=default_font,
                                   width=70,
                                   padx=150)

ram_load_percent_label = tk.Label(root,
                                  text="Объём загруженной оперативной памяти (в %):",
                                  font=default_font,
                                  padx=150)

ram_load_percent_value_label = tk.Label(root,
                                        font=default_font,
                                        width=70,
                                        padx=150)

disk_read_speed_label = tk.Label(root,
                                 text="Загрузка накопителя данных (чтение):",
                                 font=default_font,
                                 padx=150)

disk_read_speed_value_label = tk.Label(root,
                                       font=default_font,
                                       width=70,
                                       padx=150)

disk_write_speed_label = tk.Label(root,
                                  text="Загрузка накопителя данных (запись):",
                                  font=default_font,
                                  padx=150)

disk_write_speed_value_label = tk.Label(root,
                                        font=default_font,
                                        width=70,
                                        padx=150)

gpu_load_percent_label = tk.Label(root,
                                  text="Загрузка ГП:",
                                  font=default_font,
                                  padx=150)

gpu_load_percent_value_label = tk.Label(root,
                                        font=default_font,
                                        width=70,
                                        padx=150)

gpu_memory_volume_label = tk.Label(root,
                                   text="Объём оперативной памяти ГП:",
                                   font=default_font,
                                   padx=150)

gpu_memory_volume_value_label = tk.Label(root,
                                         text=f"{gpu_memory_volume:.1f} МБ",
                                         font=default_font,
                                         width=70,
                                         padx=150)

gpu_memory_load_MB_label = tk.Label(root,
                                    text="Объём загруженной оперативной памяти ГП (в МБ):",
                                    font=default_font,
                                    padx=150)

gpu_memory_load_MB_value_label = tk.Label(root,
                                          font=default_font,
                                          width=70,
                                          padx=150)

gpu_memory_load_percent_label = tk.Label(root,
                                         text="Объём загруженной оперативной памяти ГП (в %):",
                                         font=default_font,
                                         padx=150)

gpu_memory_load_percent_value_label = tk.Label(root,
                                               font=default_font,
                                               width=70,
                                               padx=150)

battery_reserve_label = tk.Label(root,
                                 text="Оставшийся запас батареи:",
                                 font=default_font,
                                 padx=150)

battery_reserve_value_label = tk.Label(root,
                                       font=default_font,
                                       width=70,
                                       padx=150)

batter_status_label = tk.Label(root,
                               text="Статус батареи:",
                               font=default_font,
                               padx=150)

battery_status_value_label = tk.Label(root,
                                      font=default_font,
                                      width=70,
                                      padx=150)

battery_time_remaining_label = tk.Label(root,
                                        text="Оставшееся время работы от батареи:",
                                        font=default_font,
                                        padx=150)

battery_time_remaining_value_label = tk.Label(root,
                                              font=default_font,
                                              width=70,
                                              padx=150)

diagnostics_button = tk.Button(root,
                               command=diagnostics,
                               text="Диагностика энергопотребления",
                               font=default_font,
                               padx=150,
                               pady=10)

diagnostics_button.config(state=tk.DISABLED)

optimize_button = tk.Button(root,
                            command=optimize,
                            text="Оптимизация энергопотребления",
                            font=default_font,
                            padx=150,
                            pady=10)

optimize_button.config(state=tk.DISABLED)

cpu_cores_label.grid(row=0,
                     column=0,
                     columnspan=2)
tree.grid(row=1,
          column=0,
          columnspan=2,
          sticky=tk.NSEW)

cpu_load_label.grid(row=2,
                    column=0)

cpu_load_value_label.grid(row=2,
                          column=1)

cpu_cores_count_label.grid(row=3,
                           column=0)

cpu_cores_count_value_label.grid(row=3,
                                 column=1)

cpu_threads_label.grid(row=4,
                       column=0)

cpu_threads_value_label.grid(row=4,
                             column=1)

cpu_min_freq_label.grid(row=5,
                        column=0)

cpu_min_freq_value_label.grid(row=5,
                              column=1)

cpu_max_freq_label.grid(row=6,
                        column=0)

cpu_max_freq_value_label.grid(row=6,
                              column=1)

ram_volume_label.grid(row=7,
                      column=0)

ram_volume_value_label.grid(row=7,
                            column=1)

ram_load_MB_label.grid(row=8,
                       column=0)

ram_load_MB_value_label.grid(row=8,
                             column=1)

ram_load_percent_label.grid(row=9,
                            column=0)

ram_load_percent_value_label.grid(row=9,
                                  column=1)

disk_read_speed_label.grid(row=10,
                           column=0)

disk_read_speed_value_label.grid(row=10,
                                 column=1)

disk_write_speed_label.grid(row=11,
                            column=0)

disk_write_speed_value_label.grid(row=11,
                                  column=1)

gpu_load_percent_label.grid(row=12,
                            column=0)

gpu_load_percent_value_label.grid(row=12,
                                  column=1)

gpu_memory_volume_label.grid(row=13,
                             column=0)

gpu_memory_volume_value_label.grid(row=13,
                                   column=1)

gpu_memory_load_MB_label.grid(row=14,
                              column=0)

gpu_memory_load_MB_value_label.grid(row=14,
                                    column=1)

gpu_memory_load_percent_label.grid(row=15,
                                   column=0)

gpu_memory_load_percent_value_label.grid(row=15,
                                         column=1)

battery_reserve_label.grid(row=16,
                           column=0)

battery_reserve_value_label.grid(row=16,
                                 column=1)

batter_status_label.grid(row=17,
                         column=0)

battery_status_value_label.grid(row=17,
                                column=1)

battery_time_remaining_label.grid(row=18,
                                  column=0)

battery_time_remaining_value_label.grid(row=18,
                                        column=1)

tk.Label(root).grid(row=19,
                    column=0,
                    columnspan=2)

diagnostics_button.grid(row=20,
                        column=0)

optimize_button.grid(row=20,
                     column=1)

tk.Label(root).grid(row=21,
                    column=0,
                    columnspan=2)

update_stats()
threading.Timer(1.5, unlock_diagnostics_button).start()
root.mainloop()
