import json
from utils import path_utils


class NexusMetaData:
    def __init__(self):
        self.config_file_name = "nexus_metadata.nxs"
        self.config_data_path = path_utils.get_config_path() + self.config_file_name
        self.data = self.get_metadata()

    # ADDING DATA

    def add_new_tab(self, tab_name):
        if tab_name in self.data.keys():
            print("Tab name already exists, "
                  "Please choose a different name.")
            return
        else:
            self.data[tab_name] = {}
            self.write_metadata(self.data)
            self.data = self.get_metadata()

    def add_new_group(self, tab_name, group_name):
        if self.check_exists(tab_name=tab_name):
            if group_name in self.data[tab_name].keys():
                print("Group name in this Tab already exists, "
                      "Please choose a different name.")
                return
            else:
                self.data[tab_name][group_name] = {}
                self.write_metadata(self.data)
        else:
            raise AttributeError("Cannot add new group, try refreshing Nexus")

    def add_new_entry(self, tab_name, group_name, file_path):
        entry_dict = {"Entry": {
                     "icon": "export_icon.png",
                     "source_file": "path_to_file",
                     "metadata": "User entered notes here",
                     "file_extension": ".png"
                     }}
        if self.check_exists(tab_name=tab_name, group_name=group_name):
            entry_name = path_utils.get_file_name(file_path)
            self.data[tab_name][group_name][entry_name] = entry_dict
            # replacing default entry name
            entry_dict[entry_name] = entry_dict.pop(list(entry_dict.keys())[0])
            self.write_metadata(self.data)
        else:
            raise AttributeError("Cannot add new Entry, try refreshing Nexus")

    # REMOVING DATA

    def remove_tab(self, tab_name):
        if self.check_exists(tab_name=tab_name):
            self.data = self.get_metadata()
            self.data.pop(tab_name, None)
            self.write_metadata(self.data)
            self.data = self.get_metadata()

    def remove_group(self, tab_name, group_name):
        if self.check_exists(tab_name=tab_name, group_name=group_name):
            self.data = self.get_metadata()
            self.data[tab_name].pop(group_name, None)
            self.write_metadata(self.data)
            self.data = self.get_metadata()

    def remove_entry(self, tab_name, group_name, entry_name):
        if self.check_exists(tab_name=tab_name, group_name=group_name, entry_name=entry_name):
            self.data = self.get_metadata()
            self.data[tab_name][group_name].pop(entry_name, None)
            self.write_metadata(self.data)
            self.data = self.get_metadata()

    # GETTERS

    def get_metadata(self):
        with open(self.config_data_path) as metadata_file:
            data = json.load(metadata_file)
            return data

    def get_tab(self, tab_name):
        data = self.get_metadata()
        if self.check_exists(tab_name=tab_name):
            return data[tab_name]
        else:
            raise AttributeError("Cannot find tab: %s in NXS" % tab_name)

    def get_group(self, tab_name, group_name):
        if self.check_exists(tab_name=tab_name, group_name=group_name):
            return self.get_tab(tab_name)[group_name]
        else:
            raise AttributeError("Cannot find group: %s in NXS" % group_name)

    def get_entry(self, tab_name, group_name, entry_name):
        if self.check_exists(tab_name=tab_name, group_name=group_name, entry_name=entry_name):
            return self.get_group(tab_name, group_name)[entry_name]
        else:
            raise AttributeError("Cannot find entry: %s in NXS" % entry_name)

    # WRITING

    def write_metadata(self, data):
        with open(self.config_data_path, "w") as out:
            json.dump(data, out, indent=2)

    # UTILITIES

    def check_exists(self, tab_name="", group_name="", entry_name=""):
        data = self.get_metadata()
        if len(tab_name):
            if tab_name in data.keys():
                if len(group_name):
                    if group_name in data[tab_name].keys():
                        if len(entry_name):
                            if entry_name in data[tab_name][group_name].keys():
                                return True
                            else:
                                raise AttributeError("Entry: %s idoes not exist in this group,\n "
                                                     "Please choose a different name." % entry_name)
                                return False
                        else:
                            return True
                    else:
                        raise AttributeError("Group: %s does not exist,\n Try refreshing Nexus." % group_name)
                        return False
                else:
                    return True
            else:
                raise AttributeError("Tab: %s does not exist,\n Try refreshing Nexus." % tab_name)
                return False



data_struct = {
    # TABS
    "TAB1":
        {
            "GROUP2":
                {

                    "Test_Prop6": {
                        "icon": "export_icon.png",
                        "source_file": "path_to_file",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop7": {
                        "icon": "export_icon.png",
                        "source_file": "path_to_file",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    }
                }

        },
}

#test = NexusMetaData().write_metadata(data_struct)