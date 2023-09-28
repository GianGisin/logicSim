import configparser

config = configparser.ConfigParser()

DEFAULT_CONFIG_PATH = "config.ini"
VERSION = "0.1.0"


def load_config() -> bool:
    if config.read(DEFAULT_CONFIG_PATH):
        # config succesfully loaded
        return True
    else:
        write_default_config(DEFAULT_CONFIG_PATH)
        return False


def set_option(key: str, new_value: str):
    config["PREFERENCES"][key] = new_value

    with open(DEFAULT_CONFIG_PATH, "w") as configfile:
        config.write(configfile)


def get_option_bool(key: str) -> bool:
    return config["PREFERENCES"].getboolean(key)


def get_option(key: str) -> str:
    return config["PREFERENCES"][key]


def write_default_config(path: str):
    print("No config file found, writing defaults to config.ini")
    config["INFO"] = {"Version": VERSION, "Author": "Gian Gisin"}
    config["PREFERENCES"] = {
        "DrawDirectLines": "false",
        "ToolbarButtonStyle": "top",
    }
    with open(path, "w") as configfile:
        config.write(configfile)


if __name__ == "__main__":
    print(load_config())
