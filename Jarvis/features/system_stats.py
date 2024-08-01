import psutil

def system_stats():
    """
    This function will fetch system stats
    :return: system statistics if success, False if fail
    """
    try:
        usage = str(psutil.cpu_percent())
        battery = str(psutil.sensors_battery())
        return usage, battery
    except Exception as e:
        print(e)
        return False
