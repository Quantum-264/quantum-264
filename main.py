import quantum_os
import apps.terminal as terminal_app
import apps.i2c_scan_app as i2c_scan_app

if __name__ == '__main__':
    quantum_os.boot(terminal_app.App)