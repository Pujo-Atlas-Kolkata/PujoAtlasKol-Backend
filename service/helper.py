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
