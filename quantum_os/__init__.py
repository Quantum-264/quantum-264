from picovision import PicoVision, PEN_P5
from machine import Pin, I2C, UART, SPI
from quantum_os.display import *
from quantum_os.memory import get_free_memory


import time
import gc
import os
import sdcard

# import quantum_os.i2c_keyboard
import apps.terminal as terminal

# from quantum_os.graphics import *
# from quantum_os.expansion import *


import quantum_os.intents as intents
from quantum_os.intents import *

# from quantum_os.keycode import Keycode as keycode

from quantum_os.keyboard import Keyboard



TMP_DOWNLOAD_PLAY_APP = "/sd/download_play_app.py"

def prepare_for_launch() -> None:
    for k in locals().keys():
        if k not in ("__name__",
                     "application_file_to_launch",
                     "gc"):
            del locals()[k]
    gc.collect()

def get_internal_i2c():
    return I2C(1, scl=Pin(7), sda=Pin(6))

def get_expansion_i2c():
    return I2C(1, scl=Pin(1), sda=Pin(0))

def get_expansion_uart(baudrate=115200):
    return UART(0, baudrate, tx=Pin(0), rx=Pin(1))
    
def get_sdcard():
    sd_spi = SPI(1, sck=Pin(10, Pin.OUT), mosi=Pin(11, Pin.OUT), miso=Pin(12, Pin.OUT))
    return sdcard.SDCard(sd_spi, Pin(15))

def get_applications() -> list[dict[str, str, str]]:
    applications = []
    global app
    
    app_files = os.listdir()
    download_play_app = TMP_DOWNLOAD_PLAY_APP
    
    for file in app_files:
        if file.endswith("app.py"):
            applications.append({
                "file": file[:-3],
            })
            
    try:
        os.stat(download_play_app)  # Get file information
        applications.append({
            "file": download_play_app[:-3],
            "temporary": True
        })
    except OSError:
        pass
    
    for app in applications:
        frontmatter = ""
        filename = app["file"] + ".py"
        with open(filename, 'r') as f:
            index = 0
            for line in f.readlines():
                if index == 0:
                    if not line.startswith("'"):
                        print(line)
                        print(f"[APP].MISSING_METADATA {filename}")
                        break
                if index > 0:
                    if not line.startswith("'"):
                        frontmatter += line
                    else:
                        break
                index += 1
            f.close()
                
        try:
            exec(frontmatter)
        except SyntaxError:
            print(f"[APP].SYNTAX_ERROR {filename}")

    return sorted(applications, key=lambda x: x["name"])

sd = get_sdcard()
persist = {}
os.mount(sd, "/sd")

kbd = Keyboard()

try:
    os.remove(TMP_DOWNLOAD_PLAY_APP)
    print("[qos].temp_file_removed")
except:
    print("[qos].temp_file_missing")

def boot(next_app):
            
    running_app = next_app()
    running_app_instance = None

    while True:
        kbd.update()
        if running_app:
            if not running_app_instance:
                running_app.setup(display)
                running_app_instance = running_app.run()
            intent = next(running_app_instance)
        else:
            intent = INTENT_FLIP_BUFFER
            
        if is_intent(intent, INTENT_KILL_APP):
            running_app = None
            running_app_instance = None
            print("[QOS].APP_KILLED")
            gc.collect()
            
            next_app = terminal.App
            if len(intent) == 2:
                # imp = importlib.import_module("apps.scan_app")
                # print("apps.scan_app", imp)
                imp = __import__("apps.scan_app")  # Import the top-level 'apps' module
                scan_app = getattr(imp, "scan_app", None)  # Retrieve 'scan_app' submodule
                print("scan_app", scan_app)

                next_app = scan_app.App

                # next_app = imp.App
                # next_app = __import__(intent[1]["file"], fromlist=["App"]).App
            running_app = next_app()
            
        if is_intent(intent, INTENT_NO_OP):
            pass
        
        
        if is_intent(intent, INTENT_FLIP_BUFFER):
            draw_border()
            
            display.update()