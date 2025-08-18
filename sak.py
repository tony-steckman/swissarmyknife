""" Main entry point for the Swiss Army Knife application. """

import importlib
import inspect
import pkgutil
import sys

from src.lib.tool import Tool


def load_module(tool_name):
    """Dynamically load a tool module by name."""
    try:
        module = importlib.import_module(f"src.tools.{tool_name}")
        return module
    except ImportError as e:
        print(f"Tool '{tool_name}' could not be loaded: {e}")


def load_tool(tool_name):
    """Load a tool class from a module by name."""
    module = load_module(tool_name)
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, Tool) and obj is not Tool:
            return obj
    print(f"No valid tool class found in module '{tool_name}'.")


def run_tool(tool_instance):
    """Run a tool by its name."""
    if not isinstance(tool_instance, Tool):
        return "Please provide the name of a valid, loaded tool."
    return tool_instance.run()


def prompt(loaded_tools=None):
    """Return the command prompt for the Swiss Army Knife application."""
    if not loaded_tools:
        loaded_tools = {}
    command = input("swiisarmyknife> ").split(" ")
    if command[0] == "list":
        if len(command) == 1 or command[1] == "tools":
            tools = list_tools()
            print("Available tools:", ", ".join(tools))
        elif command[1] == "loaded":
            if loaded_tools:
                print("Loaded tools:", ", ".join(loaded_tools.keys()))
            else:
                print("No tools are currently loaded.")
    elif command[0] == "load" and len(command) > 1:
        if command[1] in loaded_tools.keys():
            print(f"Tool '{command[1]}' is already loaded.")
        try:
            tool_class = load_tool(command[1])
            tool_instance = tool_class()
            loaded_tools[command[1]] = tool_instance
            print(f"Tool '{command[1]}' loaded successfully.")
        except (ImportError, AttributeError, TypeError) as e:
            print(f"Error loading tool '{command[1]}': {e}")
    elif command[0] == "run" and len(command) > 1:
        if command[1] not in loaded_tools:
            print(
                f"Tool '{command[1]}' is not loaded. "
                f"Use 'load {command[1]}' first."
            )
        else:
            result = run_tool(loaded_tools[command[1]])
            print(f"Result from '{command[1]}': {result}")
    elif command[0] == "exit":
        print("Exiting Swiss Army Knife application.")
        sys.exit(0)
    else:
        print(f"Unknown command: {command[0]}. "
              f"Type 'help' for available commands.")

    prompt(loaded_tools)


def list_tools():
    """List all available tools in the src.tools package."""
    tools = []
    package = importlib.import_module("src.tools")
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        tools.append(module_name)
    return tools


def main():
    """Main function to run the Swiss Army Knife application."""
    print("Welcome to the Swiss Army Knife application!")
    prompt()


if __name__ == "__main__":
    main()
