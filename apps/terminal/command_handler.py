import machine
import quantum_os
from quantum_os.constants import *
from quantum_os.display import *
from quantum_os.memory import get_free_memory


class CommandHandler: 
    """Handle the execution of commands."""
    def __init__(self, terminal):
        from apps.terminal import App as Terminal
        self.terminal: Terminal = terminal
        self.selected_app = 0
        self.buffer = ""
        self.command = ""
        self.history = []
        
        self.commands = {
            "clr": {"aliases": ["clr", "-c"], "args": [], "description": "Clear the screen", "handler": self.command_clear},
            "help": {"aliases": ["help", "-h"], "args": [], "description": "Show this help message", "handler": self.command_help},
            "apps": {"aliases": ["apps", "-a"], "args": [], "description": "List available applications", "handler": self.command_apps},
            "colors": {"aliases": ["colors", "-col"], "args": [], "description": "Display all colors", "handler": self.command_colors},
            "mem": {"aliases": ["mem", "-m" ], "args": [], "description": "Display memory usage", "handler": self.command_mem},
            "load": {"aliases": ["load", "-l"], "args": ["index"], "description": "Load an application", "handler": self.command_load},
            "reset": {"aliases": ["reset", "-r"], "args": [], "description": "Reset the device", "handler": self.command_reset},
        }


    def parse_command(self, input_command):
        """Parse input and extract command and arguments."""
        tokens = input_command.split()  # Split input into tokens
        if not tokens:
            return None, {}

        command_name = tokens[0]  # Normalize command name
        args = tokens[1:]  # Remaining tokens are arguments
        parsed_args = {}

        print("Command name: ", command_name)
        print("Args: ", args)

        # Find the matching command
        for key, cmd in self.commands.items():
            if command_name in cmd["aliases"]:
                # Parse named arguments (e.g., --option value)
                i = 0
                while i < len(args):
                    if args[i].startswith("--"):  # Named argument
                        parsed_args[args[i][2:]] = args[i + 1] if i + 1 < len(args) else True
                        i += 2
                    elif args[i].startswith("-") and len(args[i]) > 1:  # Short option
                        parsed_args[args[i][1:]] = args[i + 1] if i + 1 < len(args) else True
                        i += 2
                    else:  # Positional argument
                        parsed_args["args"] = args[i:]
                        # parsed_args.setdefault("_positional",[]).append(args[i])
                        i += 1
                return cmd["handler"], parsed_args

        return None, {}  # Unknown command

    def command_reset(self):
        """Reset the device."""
        machine.soft_reset()
        yield quantum_os.INTENT_NO_OP


    def command_unknown(self):
        """Display an unknown command message."""
        self.terminal.add_to_buffer({"text": f"Unknown command: {self.command}", "c": COLORS[2]})
        yield quantum_os.INTENT_NO_OP

    
    def command_invalid_args(self):
        """Display an invalid arguments message."""
        self.terminal.add_to_buffer({"text": f"Invalid arguments for command: {self.command}", "c": COLORS[2]})
        yield quantum_os.INTENT_NO_OP


    def command_help(self):
        """Display a list of available commands."""
        self.terminal.add_to_buffer({"text": "Available commands:", "c": COLORS[6]})
        for key, value in sorted(self.commands.items()):
            args = " ".join(map(lambda x: f"<{x}>", value["args"]))
            self.terminal.add_to_buffer({"text": f"{"  ".join(value["aliases"])}  {args} |  {value["description"]}", "c": COLORS[20]})
        yield quantum_os.INTENT_NO_OP


    def command_apps(self):
        """Display a list of available applications."""
        self.terminal.add_to_buffer({"text": "Available applications:", "c": COLORS[6]})
        for app_index, app in enumerate(self.terminal.apps):
            self.terminal.add_to_buffer({"text": f"{app_index}. {app["title"]}", "c": COLORS[4]})
        yield quantum_os.INTENT_NO_OP


    def command_clear(self):
        """Clear the text buffer."""
        self.terminal.line_buffer = []
        yield quantum_os.INTENT_NO_OP


    def command_colors(self):
        """Display all colors."""
        self.terminal.add_to_buffer({"cmd": self.terminal.draw_colors})
        yield quantum_os.INTENT_NO_OP


    def command_mem(self):
        """Display memory usage."""
        self.terminal.add_to_buffer({"text": f"Free Memory: {get_free_memory()["free"]} KB", "c": COLORS[25]})
        yield quantum_os.INTENT_NO_OP


    def command_load(self, args):
        """Flag the terminal to load an application."""
        if not args:
            yield from self.command_invalid_args()
            return
        elif len(args) != 1:
            yield from self.command_invalid_args()
            return
        
        app_index = args[0]
        if app_index is None:
            yield from self.command_invalid_args()
            return
        
        app_index = int(app_index)
        self.terminal.load_app = True
        self.terminal.selected_app = app_index
        yield quantum_os.INTENT_NO_OP


    def handle_command(self):
        """Handle user input and execute commands."""
        # Remove leading/trailing spaces
        self.command = self.buffer.strip()
        # Clear command buffer
        self.buffer = ""  
        # Add command to text buffer
        self.terminal.add_to_buffer({"text": f">{self.command}", "c": COLORS[3], "o": -10})

        handler, args = self.parse_command(self.command)

        if handler:
            yield from handler(**args)                
        else:
            yield from self.command_unknown()

    
        display.remove_clip()
        yield quantum_os.INTENT_NO_OP