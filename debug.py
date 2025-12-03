DEBUG = True

def print_debug_message(*args, **kwargs):
    if DEBUG:
        print("DEBUG")
        print(*args, **kwargs)