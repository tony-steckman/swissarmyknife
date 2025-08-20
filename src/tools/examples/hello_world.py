"""A simple tool that prints 'Hello, World!'.   """

from src.lib.tool import Tool


class HelloWorldTool(Tool):
    """A simple tool that prints 'Hello, World!'.   """

    def __init__(self):
        super().__init__(
            name="HelloWorld",
            description="A simple tool that prints 'Hello, World!'",
            version="1.0.0",
            author="Tony Steckman"
        )
        self.add_output("greeting")
        self.add_optional_input("name")

    def run(self):
        """Execute the tool's main functionality."""
        name = self.input_values.get("name", "World")
        greeting = f"Hello, {name}!"
        self.output_values['greeting'] = greeting
        return self.output_values['greeting']
