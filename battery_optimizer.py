import subprocess

POWER_SCHEME_HIGH_PERFORMANCE = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
POWER_SCHEME_BALANCED = "381b4222-f694-41f0-9685-ff5bb260df2e"
POWER_SCHEME_POWER_SAVER = "a1841308-3541-4fab-bc81-f71556f20b4a"


def set_power_scheme(power_scheme_guid):
    command = f"powercfg /setactive {power_scheme_guid}"
    subprocess.run(["powershell", "-Command", command], capture_output=True)


def set_power_scheme_high_performance():
    set_power_scheme(POWER_SCHEME_HIGH_PERFORMANCE)


def set_power_scheme_balanced():
    set_power_scheme(POWER_SCHEME_BALANCED)


def set_power_scheme_power_saver():
    set_power_scheme(POWER_SCHEME_POWER_SAVER)


def get_current_power_scheme_guid():
    command = "powercfg /getactivescheme"
    result = subprocess.run(["cmd", "/c", command], capture_output=True, text=True)
    return result.stdout.strip()


def check_power_scheme():
    global POWER_SCHEME_BALANCED
    global POWER_SCHEME_POWER_SAVER
    global POWER_SCHEME_HIGH_PERFORMANCE
    current_scheme_guid = get_current_power_scheme_guid()
    if POWER_SCHEME_POWER_SAVER in current_scheme_guid:
        return 1
    elif POWER_SCHEME_BALANCED in current_scheme_guid:
        return 2
    elif POWER_SCHEME_HIGH_PERFORMANCE in current_scheme_guid:
        return 3
    else:
        return 0
