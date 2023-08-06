# yaconfig

Python package to assist configuration of Python software.


## Installation
To install the latest release:
```bash
pip3 install yaconfig
```

## Usage
This package is intended to be used by other package to assist their configuration. The recommended workflow follows:
- Add a config module. Its purpose should be to define the configuration variables (the metaconfig) and to provide a
single instance of the actual configuration (the values) for your application. If you want to implement a more complex
logic to handle multiple configuration, you can do it here. Simple example:
```python
# File config.py
import yaconfig

metaconfig = yaconfig.MetaConfig(
    yaconfig.Variable("text", type=str, default="Hello world", help="Text to output")
)


# Get a default configuration, which should be overridden when the execution starts
config = yaconfig.Config(metaconfig)
```

- In the entry point of your program, load the previous module and initialize the config using the desired method.
The variables can be accessed from now on. Example:
```python
# File main.py
from config import config  # Just need the config object of the previous module 

try:
    config.load_json("config.json")
except FileNotFoundError:
    print("config.json file not found. Using the default configuration instead.")

print(config["text"])
```
Note that if that file can be loaded as a module, you should avoid initializing the config. You can use ```__main__``` or
build a launching script to prevent this.

- To document the configuration, you can use the methods of the metaconfig variable you have defined. This can be done
manually from the interpreter or automated by writing a script. Some examples follow:
```python
from config import metaconfig

metaconfig.generate_json_example()  # Generate a conf.example.json file
metaconfig.generate_environment_example()  # Generate a environment.sh file
```
