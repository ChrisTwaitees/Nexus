import os
import ntpath

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


def get_extension(path):
    return os.path.splitext(path)[1]


def get_file_name(path):
    path = get_os_path(path)
    # check for file extension, if none, return folder name
    if not len(ntpath.splitext(path)[1]):
        return ntpath.split(path)[1]
    else:
        return ntpath.split(path)[1].split(".")[0]

