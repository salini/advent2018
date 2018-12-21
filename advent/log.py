
_LOG=False

def show_log(enable):
    _LOG=enable

def log(msg):
    if _LOG:
        print msg