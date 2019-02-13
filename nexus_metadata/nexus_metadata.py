import json
from utils import path_utils


class NexusMetaData:
    def __init__(self):
        self.config_file_name = "nexus_metadata.nxs"
        self.config_data_path = path_utils.get_config_path() + self.config_file_name
        self.data = self.get_metadata()

    def add_new_tab(self, tab_name):
        if tab_name in self.data.keys():
            print("Tab name already exists, "
                  "Please choose a different name.")
        else:
            self.data[tab_name] = {}
            self.write_metadata(self.data)
            self.data = self.get_metadata()

    def remove_tab(self, tab_name):
        self.data.pop(tab_name, None)
        self.write_metadata(self.data)
        self.data = self.get_metadata()

    def add_new_group(self, tab_name, group_name):
        if tab_name not in self.data.keys():
            print("Tab does not exist, cannot add new group")
            return
        elif group_name in self.data[tab_name].keys():
            print("Group name in this Tab already exists, "
                  "Please choose a different name.")
            return
        else:
            self.data[tab_name][group_name] = {}
            self.write_metadata(self.data)

    def add_new_entry(self, tab_name, group_name, entry_name):
        entry_dict =    {"Entry": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        #TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                        }}
        if tab_name not in self.data.keys():
            print("Tab does not exist")
            return
        elif group_name not in self.data[tab_name].keys():
            print("Group does not exist, cannot add new Entry")
        elif entry_name in self.data[tab_name][group_name].keys():
            print("Entry name in this Group already exists, "
                  "Please choose a different name.")
        else:
            self.data[tab_name][group_name][entry_name] = {}
            self.write_metadata(self.data)

    def get_metadata(self):
        with open(self.config_data_path) as metadata_file:
            data = json.load(metadata_file)
            return data

    def write_metadata(self, data):
        with open(self.config_data_path, "w") as out:
            json.dump(data, out, indent=2)



data_struct = {
    # TABS
    "TAB1":
        {
            # GROUPS
            "GROUP1":
            {
            },
            "GROUP2":
                {
                    # ENTRY example
                    "Test_Prop2": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop3": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop4": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    }
                },
            "GROUP2":
                {
                    # ENTRY example
                    "Test_Prop5": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop6": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop7": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    }
                }

        },
    "TAB2":
        {
            # GROUPS
            "GROUP1":
                {
                    # ENTRY example
                    "Test_Prop": {
                        "icon_name": "refresh_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    }
                },
            "GROUP2":
                {
                    # ENTRY example
                    "Test_Prop2": {
                        "icon_name": "refresh_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop3": {
                        "icon_name": "",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop4": {
                        "icon_name": "refresh_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    }
                },
            "GROUP2":
                {
                    # ENTRY example
                    "Test_Prop5": {
                        "icon_name": "refresh_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop6": {
                        "icon_name": "refresh_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop7": {
                        "icon_name": "voronoi.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "path_to_file",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    }
                }

        },
    "TAB3":
        {
            # GROUPS
            "GROUP1":
                {
                    # ENTRY example
                    "Test_Prop": {
                        "icon_name": "voronoi.png",
                        "icon_location": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    }
                },
            "GROUP2":
                {
                    # ENTRY example
                    "Test_Prop2": {
                        "icon_name": "voronoi.png",
                        "icon_location": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop3": {
                        "icon_name": "",
                        "icon_location": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop4": {
                        "icon_name": "voronoi.png",
                        "icon_location": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    }
                },
            "GROUP3":
                {
                    # ENTRY example
                    "Test_Prop5": {
                        "icon_name": "voronoi.png",
                        "icon_location": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop6": {
                        "icon_name": "voronoi.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop7": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    }
                },
            "GROUP3":
                {
                    # ENTRY example
                    "Test_Prop5": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop6": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop7": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop8": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop9": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop10": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop11": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop12": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    },
                    "Test_Prop13": {
                        "icon_name": "export_icon.png",
                        "icon_location": "",
                        # TODO fetch owner of file
                        "owner": "User",
                        "local_source_file": "G:\Forgotten Snow White\WIP\Hair\hair_02.PNG",
                        "virtual_file_location": "Perforce_path",
                        "metadata": "User entered notes here",
                        "file_extension": ".png"
                    }
                }

        }
}

#test = NexusMetaData().write_metadata(data_struct)