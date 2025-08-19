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
        try:
            tool_instance.load_configuration()
            if tool_instance.configurations:
                print(f"Configuration for '{command[1]}' loaded successfully.")
        except (IOError, OSError) as e:
            print(f"Error loading configuration for '{command[1]}': {e}")
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
    elif command[0] in loaded_tools.keys() and len(command) > 1:
        tool_instance = loaded_tools[command[0]]
        if command[1] == "get" and len(command) > 2:
            if command[2] == "inputs":
                print("Required inputs:", tool_instance.required_inputs)
                print("Optional inputs:", tool_instance.optional_inputs)
                print("Values:", tool_instance.input_values)
            elif command[2].startswith("config"):
                print(
                    f"Configuration for '{tool_instance.name}': "
                    f"{tool_instance.configurations}"
                )
            else:
                print(f"Unknown input type: {command[2]}. "
                      f"Available inputs: inputs, configs.")
        elif command[1] == "info":
            print(f"Tool Name: {tool_instance.name}")
            print(f"Description: {tool_instance.description}")
            print(f"Version: {tool_instance.version}")
            print(f"Author: {tool_instance.author}")
            print(f"Required Inputs: {tool_instance.required_inputs}")
            print(f"Optional Inputs: {tool_instance.optional_inputs}")
            print(
                f"Configuration Parameters: "
                f"{tool_instance.configuration_parameters}"
            )
        elif command[1] == "run":
            result = run_tool(tool_instance)
            print(f"Result from '{tool_instance.name}': {result}")
        elif command[1] == "save" and len(command) > 2:
            if command[2].startswith("config"):
                tool_instance.save_configuration()
                print(f"Configuration for '{tool_instance.name}' saved.")
            else:
                print(f"Unknown save type: {command[2]}. "
                      f"Available types: configs.")
        elif command[1] == "load" and len(command) > 2:
            if command[2].startswith("config"):
                tool_instance.load_configuration()
                print(f"Configuration for '{tool_instance.name}' loaded.")
            else:
                print(f"Unknown load type: {command[2]}. "
                      f"Available types: configs.")
        elif command[1] == "set" and len(command) > 3:
            input_name = command[2]
            value = " ".join(command[3:])
            try:
                tool_instance.set_input_value(input_name, value)
                print(f"Input '{input_name}' set to '{value}'.")
            except ValueError as e:
                print(e)
        else:
            print(f"Unknown command for tool '{command[0]}': {command[1]}. "
                  f"Available commands: get, info, run, set.")
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
