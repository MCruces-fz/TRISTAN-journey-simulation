import json
import os
from os.path import join as join_path

from utils.constants import ROOT_DIR


class CookAiresINP:
    def __init__(self, task_name, save_path=None):
        with open("utils/config.json", "r") as config_file:
            configuration = json.load(config_file)
        self.config = configuration

        with open("utils/input_template.txt", "r") as template:
            content = template.read().format(task_name=task_name, **self.config["template"])
        self.content_str = content

        self.save_model(save_path, task_name)

    def save_model(self, save_path, task_name):
        if save_path is not None:
            save_in = save_path
        else:
            save_in = ROOT_DIR
        with open(join_path(save_in, f"{task_name}.inp"), 'w+') as f:
            f.write(self.content_str)


if __name__ == "__main__":
    CookAiresINP("TestTask")
