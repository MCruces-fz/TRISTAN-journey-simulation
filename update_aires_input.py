import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

with open("input_template.txt", "r") as template:
    content = template.read().format(**config["template"])
    print(content)

