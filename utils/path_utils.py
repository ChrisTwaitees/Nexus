import os

scriptDir = os.path.dirname(os.path.realpath(__file__))
solutionName = "Skat"

def return_icon_path(icon_name):
    return (scriptDir.split(solutionName)[0] + os.path.join(solutionName, "data", "icons", "") + icon_name)

def return_formatted_path(path):
    return os.path.normpath(r"%s"%path)

