"""
Author: Miguel Cruces
e-mails:
- miguel.cruces.fernandez@usc.es
- mcsquared.fz@gmail.com
"""

from update_model import CookModel
from update_tables import CookTables
from update_aires_input import CookAiresINP
from represent import CookingDataAIRES, Represent
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
input_df = pd.read_csv("HeightDensData.txt", index_col=0, header=0, delim_whitespace=True, na_values="(missing)")

# First, we create the directory ROOT_DIR/AiresINP:
aires_inp_path = join_path(ROOT_DIR, "AiresINP")
if not os.path.exists(aires_inp_path):
    os.mkdir(aires_inp_path)

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

for task in os.listdir(aires_inp_path):
    task_full_dir = join_path(aires_inp_path, task)
    for file in os.listdir(task_full_dir):
        if file[-6:-4] == ".t":
            output_full_path = join_path(ROOT_DIR, "OUTPUT")
            if not os.path.exists(output_full_path):
                os.mkdir(output_full_path)
            data = CookingDataAIRES(in_path=task_full_dir, file=file)
            Represent(data, out_path=output_full_path, task_name=task)
