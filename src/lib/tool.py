"""
Define a class representing a tool with metadata, including inputs and outputs.
"""


import keyring

from src.lib.sqlite import Database


class Tool:
    """
    A class representing a tool with metadata.
    """

    def __init__(self, name, description, version, author):
        self.name = name
        self.description = description
        self.version = version
        self.author = author
        self.required_inputs = []  # List of required inputs for the tool
        self.optional_inputs = []  # List of optional inputs for the tool
        self.outputs = []  # List of outputs produced by the tool
        self.input_values = {}  # Dictionary to hold input values
        self.output_values = {}  # Dictionary to hold output values
        # List of configuration parameters for the tool
        self.configuration_parameters = []
        # Dictionary to hold configurations for the tool
        self.configurations = {}
        # Dictionary to hold credentials for the tool
        self.credentials = {}

    def add_required_input(self, input_name):
        """
        Adds a required input to the tool.

        :param input_name: Name of the required input
        """
        self.required_inputs.append(input_name)

    def add_optional_input(self, input_name):
        """
        Adds an optional input to the tool.

        :param input_name: Name of the optional input
        """
        self.optional_inputs.append(input_name)

    def add_output(self, output_name):
        """
        Adds an output to the tool.
        """
        self.outputs.append(output_name)

    def set_input_value(self, input_name, value):
        """
        Sets the value for a given input.

        :param input_name: Name of the input
        :param value: Value to set for the input
        """
        if (
            input_name in self.required_inputs
            or input_name in self.optional_inputs
        ):
            self.input_values[input_name] = value
        else:
            raise ValueError(
                f"Input '{input_name}' is not defined for this tool.")

    def set_output_value(self, output_name, value):
        """
        Sets the value for a given output.

        :param output_name: Name of the output
        :param value: Value to set for the output
        """
        if output_name in self.outputs:
            self.output_values[output_name] = value
        else:
            raise ValueError(
                f"Output '{output_name}' is not defined for this tool.")

    def add_configuration_parameter(self, parameter_name):
        """
        Adds a configuration parameter to the tool.

        :param parameter_name: Name of the configuration parameter
        """
        self.configuration_parameters.append(parameter_name)

    def set_configuration(self, parameter_name, value):
        """
        Sets a configuration for the tool.

        :param parameter_name: Name of the configuration parameter
        :param value: Value to set for the configuration
        """
        if parameter_name in self.configuration_parameters:
            self.configurations[parameter_name] = (
                value
            )
        else:
            raise ValueError(
                f"Configuration parameter '{parameter_name}' is not "
                f"defined for this tool."
            )

    def load_configuration(self):
        """
        Loads the configuration for the tool.
        This method can be overridden by subclasses to implement specific
        loading logic.
        """
        db = Database("dbs/tools.db")
        db.connect()
        try:
            for param in self.configuration_parameters:
                query = (
                    "SELECT value FROM configurations "
                    "WHERE tool-name = ? AND parameter = ?"
                )
                result = db.execute_query(query, (self.name, param))
                if result:
                    self.configurations[param] = result[0][0]
        finally:
            db.close()

    def save_configuration(self):
        """
        Saves the configuration for the tool.
        This method can be overridden by subclasses to implement specific
        saving logic.
        """
        db = Database("dbs/tools.db")
        db.connect()
        try:
            for param, value in self.configurations.items():
                query = (
                    "INSERT OR REPLACE INTO configurations "
                    "(tool-name, parameter, value) VALUES (?, ?, ?)"
                )
                db.execute_query(query, (self.name, param, value))
            db.commit()
        finally:
            db.close()

    def add_credentials(self, username, password):
        """
        Adds credentials for the tool.

        :param username: Username for the credentials
        :param password: Password for the credentials
        """
        self.credentials['username'] = username
        keyring.set_password(
            self.name, username, password
        )

    def get_credentials(self):
        """
        Retrieves credentials for the tool.

        :param username: Username for which to retrieve the password
        :return: Password for the given username
        """
        username = self.credentials.get('username')
        if not username:
            raise ValueError("No username set for credentials.")
        # Retrieve the password from the keyring
        self.credentials['password'] = keyring.get_password(
            self.name, username
            )
        return self.credentials

    def run(self):
        """
        Runs the tool's main functionality.
        This method should be overridden by subclasses to implement specific
        tool logic.
        """
        raise NotImplementedError("Subclasses must implement the run method.")

    def __repr__(self):
        return (
            f"Tool(name={self.name}, description={self.description}, "
            f"version={self.version}, author={self.author}, "
            f"required_inputs={self.required_inputs}, "
            f"optional_inputs={self.optional_inputs}, outputs={self.outputs}"
        )
