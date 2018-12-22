
_LOG=False

def show_log(enable):
    global _LOG
    _LOG=enable

def log(msg):
    if _LOG:
        print msg