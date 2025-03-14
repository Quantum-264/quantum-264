import quantum_os
import apps.terminal as terminal_app
import apps.scan_app as scan_app

if __name__ == '__main__':
    quantum_os.boot(terminal_app.App)