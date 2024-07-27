import time
import psutil
import GPUtil

CPU_LOAD_PER_CORE = None
DISK_IO_START = None
DISK_IO_END = None


def get_cpu_load_per_core_percent():
    global CPU_LOAD_PER_CORE
    CPU_LOAD_PER_CORE = psutil.cpu_percent(interval=1, percpu=True)
    return CPU_LOAD_PER_CORE


def get_cpu_load_summary_percent():
    global CPU_LOAD_PER_CORE
    return sum(CPU_LOAD_PER_CORE) / len(CPU_LOAD_PER_CORE)


def get_cpu_cores_number():
    return psutil.cpu_count(logical=False)


def get_cpu_threads_number():
    return psutil.cpu_count(logical=True)


def get_cpu_min_freq():
    return psutil.cpu_freq().min


def get_cpu_max_freq():
    return psutil.cpu_freq().max


def get_ram_volume_mb():
    return psutil.virtual_memory().total / 1024 ** 2  #MB


def get_ram_load_mb():
    return psutil.virtual_memory().used / 1024 ** 2  #MB


def get_ram_load_percent():
    return psutil.virtual_memory().percent


def get_disk_avg_read_speed():
    global DISK_IO_START
    global DISK_IO_END
    DISK_IO_START = psutil.disk_io_counters()
    time.sleep(1)
    DISK_IO_END = psutil.disk_io_counters()
    read_speed = (DISK_IO_END.read_bytes - DISK_IO_START.read_bytes) / 1024 ** 2  #MB/s
    return read_speed


def get_disk_avg_write_speed():
    global DISK_IO_START
    global DISK_IO_END
    write_speed = (DISK_IO_END.write_bytes - DISK_IO_START.write_bytes) / 1024 ** 2  #MB/s
    return write_speed


def get_gpu_load_percent():
    gpus = GPUtil.getGPUs()
    if gpus:
        return gpus[0].load * 100


def get_gpu_memory_volume_mb():
    gpus = GPUtil.getGPUs()
    if gpus:
        return sum([gpu.memoryTotal for gpu in gpus])  #MB


def get_gpu_memory_load_mb():
    gpus = GPUtil.getGPUs()
    if gpus:
        return sum([gpu.memoryUsed for gpu in gpus])  #MB


def get_gpu_memory_load_percent():
    gpus = GPUtil.getGPUs()
    if gpus:
        return sum([gpu.memoryUsed for gpu in gpus]) / sum([gpu.memoryTotal for gpu in gpus]) * 100


def get_battery_reserve_percent():
    battery = psutil.sensors_battery()
    return battery.percent


def get_battery_time_reserve():
    battery = psutil.sensors_battery()
    return battery.secsleft / 3600  #Hours


def get_battery_status():
    battery = psutil.sensors_battery()
    if battery.power_plugged:
        return True
    else:
        return False
