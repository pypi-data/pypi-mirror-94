"""yaconfig - Python package to assist configuration"""

__version__ = '0.3.0'
__author__ = 'Dih5 <dihedralfive@gmail.com>'

import json
import os
from collections import OrderedDict
from shlex import quote


def _quote_sh(s):
    return quote(s.replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r").replace("\0", "\\0"))


class Variable:
    """Abstraction for a variable in the configuration"""

    def __init__(self, name, type=str, default=None, help=None):
        """

        Args:
            name (str): A name identifying the variable.
            type (type): A python type to transform the value to.
            default (str): A default value, always as a string.
            help (str): A text describing what the value does.
        """
        self.name = name
        self.type = type
        self.default = default
        self.help = help

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def get(self, key, default=None):
        try:
            return self.__getattribute__(key)
        except AttributeError:
            return default

    def _get_bash(self, prefix="", value=None):
        if self.help:
            text = "# %s\n" % self.help
        else:
            text = ""

        modified_name = prefix + self.name.upper()
        if self.default:
            text += "export %s=%s" % (modified_name, _quote_sh(self.default if value is None else value))
        else:
            text += "# export %s=<value>" % modified_name
        return text


class MetaConfig:
    """An abstraction defining what is expected in a configuration"""

    def __init__(self, *variables):
        """

        Args:
            *variables (Variable): Ordered sequence of variables. Their names should be unique.

        """
        self.variables = variables
        self.variables = OrderedDict()
        for variable in variables:
            name = variable["name"]
            if name in self.variables:
                raise Variable("Variable %s defined multiple times" % name)
            self.variables[name] = variable

    def __getitem__(self, key):
        return self.variables[key]

    def __contains__(self, key):
        return key in self.variables

    def items(self):
        return self.variables.items()

    def prompt(self):
        """Prompt the user in the command line to generate configuration values"""
        output_values = {}
        for key, var in self.items():
            default = var.get("default", "")
            help_text = var.get("help", "")
            print("%s%s [%s]: " % (help_text + "\n" if help_text else "", key, default if default else "<not set>"),
                  end="\n")
            value = input()
            output_values[key] = value if value else default

        return output_values

    def generate_json_example(self, path="config.example.json", utf8=True):
        """Generate an example json configuration file"""
        values = {key: val.get("default", "") for key, val in self.items()}
        json_string = json.dumps(values, ensure_ascii=not utf8, indent=4)

        if path is not None:
            with open(path, "w") as f:
                f.write(json_string)
        else:
            return json_string

    def interactive_json(self, path="config.json", utf8=True):
        """Interactively generate a json configuration file"""
        values = self.prompt()
        json_string = json.dumps(values, ensure_ascii=not utf8, indent=4)

        if path is not None:
            with open(path, "w") as f:
                f.write(json_string)
        else:
            return json_string

    def generate_environment_example(self, path="environment.example.sh", prefix=""):
        """Generate an example bash configuration file"""
        text = "#!/bin/bash\n"
        text += "# Example configuration file\n\n"
        text += "\n\n".join(variable._get_bash(prefix=prefix) for _, variable in self.items())
        text += "\n"
        if path is None:
            return text
        else:
            with open(path, "w") as f:
                f.write(text)

    def interactive_environment(self, path="environment.sh", prefix=""):
        values = self.prompt()
        text = "#!/bin/bash\n"
        text += "\n\n".join(variable._get_bash(prefix=prefix, value=values[var_name]) for var_name, variable in self.items())
        text += "\n"
        if path is None:
            return text
        else:
            with open(path, "w") as f:
                f.write(text)



class Config:
    """A configuration"""

    def __init__(self, metaconfig):
        """

        Args:
            metaconfig (MetaConfig): The description of what is expected in this configuration

        """
        self.metaconfig = metaconfig
        self.config = {}

        self._load_defaults()

    def __getitem__(self, key):
        return self.config[key]

    def __contains__(self, key):
        return key in self.config

    def get(self, key, value=None):
        """Get the value of the selected parameter, returning a default value if not found"""
        try:
            return self.config[key]
        except KeyError:
            return value

    def items(self):
        return self.config.items()

    def load_variable(self, variable, value):
        """
        Store a value for a variable in the configuration.

        Args:
            variable: The variable name.
            value (str): Its value represented as a string.

        """
        if variable in self.metaconfig:
            t = self.metaconfig[variable].get("type", str)
            if t == bytes:
                value = bytes(value, "utf8")
            elif t == bool:
                value = value.lower()
                if value == "true":
                    value = True
                elif value == "false":
                    value = False
                else:
                    raise ValueError("Expected boolean value, found instead: %s" % value)
            else:
                value = t(value)
            self.config[variable] = value

    def _load_defaults(self):
        """Generate the default configuration"""
        for variable, settings in self.metaconfig.items():
            value = settings.get("default")
            if value is not None:
                self.load_variable(variable, value)

    def load_json(self, path):
        """
        Load the configuration from a json file

        Args:
            path (str): Path to the json file.

        """
        file = json.load(open(path, "r"))
        for variable, value in file.items():
            self.load_variable(variable, value)

    def load_environment(self, prefix=""):
        """
        Load the configuration from environment variables

        Args:
            prefix (str): A prefix for the environment variables.

        """
        for variable, value in self.metaconfig.items():
            value = os.getenv(prefix + variable.upper())
            if value is not None:
                self.load_variable(variable, value)
