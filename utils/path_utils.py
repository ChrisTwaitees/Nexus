import os

scriptDir = os.path.dirname(os.path.realpath(__file__))
solutionName = "Nexus"


def get_icon_path(icon_name=""):
    return (scriptDir.split(solutionName)[0] + os.path.join(solutionName, "data", "icons", "") + icon_name)


def get_os_path(path):
    return os.path.normpath(r"%s"%path)


def get_config_path():
    config_path = scriptDir.split(solutionName)[0] + os.path.join(solutionName, "data", "config", "")
    if os.path.exists(config_path):
        return config_path
    else:
        os.mkdir(config_path)
        return config_path

print(get_icon_path())