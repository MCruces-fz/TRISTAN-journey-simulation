"""
Author: Miguel Cruces
e-mails:
- miguel.cruces.fernandez@usc.es
- mcsquared.fz@gmail.com
"""

from update_model import CookModel
from update_tables import CookTables
from update_aires_input import CookAiresINP
from represent import CookingDataAIRES, MergeData, Represent
import json
import os
import sys
from os.path import join as join_path

import pandas as pd

# Root Directory of the Project
ROOT_DIR = os.path.abspath("./")

# Add ROOT_DIR to $PATH
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Read Configurations from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Read input data
input_df = pd.read_csv("TRISTAN_data_000.txt", index_col=0, header=0, delim_whitespace=True, na_values="(missing)")

# First, we create the directory ROOT_DIR/AiresINP:
aires_inp_path = join_path(ROOT_DIR, "AiresINP")
if not os.path.exists(aires_inp_path):
    os.mkdir(aires_inp_path)

# And the directory ROOT_DIR/OUTPUT:
output_full_path = join_path(ROOT_DIR, "OUTPUT")
if not os.path.exists(output_full_path):
    os.mkdir(output_full_path)


def call_merger(ons: list):
    """
    Merges data from the list of muons(+), muons(-), positrons(+) and electrons(-)
    :param ons: list of dictionaries {"path": "...", "file": ...}
    :return: It is a void function.
    """
    if len(ons) == 2:
        ons0 = CookingDataAIRES(in_path=ons[0]["path"], file=ons[0]["file"])
        ons1 = CookingDataAIRES(in_path=ons[1]["path"], file=ons[1]["file"])
        merged_ons = MergeData(ons0, ons1)
        Represent(merged_ons, out_path=output_full_path, task_name=task)
    elif len(ons) == 1:
        ons = CookingDataAIRES(in_path=ons[0]["path"], file=ons[0]["file"])
        Represent(ons, out_path=output_full_path, task_name=task)
    else:
        print("There aren't particles to merge data")


# Now inside AiresINP, the directories for any simulation
for row in input_df.iterrows():
    dir_name = row[0]  # Date is the name for any directory of simulation
    dir_path = join_path(aires_inp_path, dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # Create model.inp
    CookModel(save_path=dir_path,
              atm_ident=config["model"]["atm_ident"],
              atm_name=config["model"]["atm_name"],
              grd_temp=row[1]["Temp-0"])  # config["model"]["grd_temp"])
    # Create tables.inp
    CookTables(save_path=dir_path,
               print_ids=config["tables"]["print"],
               export_ids=config["tables"]["export"])
    # Create task.inp
    CookAiresINP(task_name=dir_name, save_path=dir_path)

    # Execute Aires
    os.system(f"cd {dir_path}; Aires < {dir_name}.inp")  # It Works
    break  # Only First Simulation

# For any task are crated the histograms and saved on ROOT_DIR/OUTPUT
for task in os.listdir(aires_inp_path):
    task_full_dir = join_path(aires_inp_path, task)
    trons = []  # trons: positrons (+), electrons (-)
    muons = []  # muons: muons (+), muons (-)
    for file in os.listdir(task_full_dir):
        if file[-6:-4] == ".t":
            if file.endswith("2505") or file.endswith("2506"):
                trons.append({"path": task_full_dir, "file": file})
            elif file.endswith("2507") or file.endswith("2508"):
                muons.append({"path": task_full_dir, "file": file})
            elif file.endswith("5513"):
                pass
            else:
                try:
                    data = CookingDataAIRES(in_path=task_full_dir, file=file, e_units=config["plots"]["E_units"])
                    Represent(data, out_path=output_full_path, task_name=task)
                    print(f"Represented {file}")
                except KeyError:
                    print(f"Some error in CookingDataAires with file {file}")
    # For any task: muons(+) and muons(-), positrons(+) and electrons(-) are merged
    call_merger(muons)
    call_merger(trons)
