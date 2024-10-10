import os
import time


def kb_to_mb(kb_value):
    kb_value_cleaned = kb_value.strip().replace(" kB", "")
    return float(kb_value) / 1024


def bytes_to_mb(value):
    return float(value) / (1024**2)


def mb_to_gb(mb_value):
    return float(mb_value) / 1024


def get_memory_info():
    mem_info = {}

    # Open and read the /proc/meminfo file
    with open("/proc/meminfo", "r") as f:
        for line in f:
            # Split each line into key-value pairs
            parts = line.split(":")
            key = parts[0].strip()
            value = parts[1].strip()
            mem_info[key] = value

    return mem_info


def get_disk_usage(path="/"):
    # Get the file system statistics for the specified path
    statvfs = os.statvfs(path)

    # Calculate the disk space in bytes
    total_space = statvfs.f_frsize * statvfs.f_blocks  # Total space
    free_space = statvfs.f_frsize * statvfs.f_bfree  # Free space
    # Space available to non-superuser
    available_space = statvfs.f_frsize * statvfs.f_bavail
    # Used space
    used_space = total_space - free_space

    # Convert bytes to MB
    total_space_mb = bytes_to_mb(total_space)
    free_space_mb = bytes_to_mb(free_space)
    used_space_mb = bytes_to_mb(used_space)

    return {
        "total_space_mb": total_space_mb,
        "used_space_mb": used_space_mb,
        "free_space_mb": free_space_mb,
    }


def get_cpu_usage():
    # Read the initial CPU stats
    with open("/proc/stat", "r") as f:
        first_line = f.readline()

    # Extract CPU values from the first line
    cpu_times = list(
        map(int, first_line.split()[1:])
    )  # Skip the first element (CPU label)
    total_time1 = sum(cpu_times)  # Total time spent in all states

    # Wait for a short period (1 second)
    time.sleep(1)

    # Read the CPU stats again
    with open("/proc/stat", "r") as f:
        second_line = f.readline()

    # Extract CPU values from the second line
    cpu_times = list(map(int, second_line.split()[1:]))
    total_time2 = sum(cpu_times)

    # Calculate the differences
    total_diff = total_time2 - total_time1
    idle_diff = cpu_times[3] - cpu_times[3]  # Idle time is usually the fourth value

    # Calculate CPU usage percentage
    cpu_usage = 100 * (1 - (idle_diff / total_diff))

    return cpu_usage
