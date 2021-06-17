"""
Author: Miguel Cruces
e-mails:
- miguel.cruces.fernandez@usc.es
- mcsquared.fz@gmail.com
"""

from library.update_model import CookModel
from library.update_tables import CookTables
from library.update_aires_input import CookAiresINP
from library.represent import CookingDataAIRES, MergeData, Represent, grdpcles_dat
import json
import os
import sys
from os.path import join as join_path
import numpy as np
import pandas as pd

# Root Directory of the Project
ROOT_DIR = os.path.abspath("./")

# Add ROOT_DIR to $PATH
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Read Configurations from config.json
with open("utils/config.json", "r") as config_file:
    config = json.load(config_file)

# First, we create the directory ROOT_DIR/AiresINP:
aires_inp_path = join_path(ROOT_DIR, "AiresINP")
if not os.path.exists(aires_inp_path):
    os.mkdir(aires_inp_path)

# And the directory ROOT_DIR/OUTPUT:
output_full_path = join_path(ROOT_DIR, "OUTPUT")
if not os.path.exists(output_full_path):
    os.mkdir(output_full_path)

# And the directory ROOT_DIR/SUMMARY:
sry_full_path = join_path(ROOT_DIR, "SUMMARY")
if not os.path.exists(sry_full_path) and config["SRY_dir"]:
    os.mkdir(sry_full_path)

# Read input data
input_file_name = config["InputFileName"]
input_df = None
if input_file_name.endswith(".txt"):
    input_df = pd.read_csv(input_file_name, index_col=0, header=0, delim_whitespace=True, na_values="(missing)")
elif input_file_name.endswith(".csv"):
    input_df = pd.read_csv("densidades2019.csv", index_col=0, sep=";")
else:
    quit(0)


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


# Define empty array to store angles information
hits_by_angle = np.zeros([0, 19 * 3])  # 19 bins from 0 to 95 degrees, 3 types of particles

# Now inside AiresINP, the directories for any simulation
for row in input_df.iterrows():
    dir_name = row[0]  # Date is the name for any directory of simulation (its task name)
    dir_path = join_path(aires_inp_path, dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    try:
        temp_0 = row[1]["Temp-0"]
    except Exception as e:
        temp_0 = config["model"]["grd_temp"]

    # Create file model.inp
    CookModel(save_path=dir_path,
              input_df_row=row[1],
              atm_ident=config["model"]["atm_ident"],
              atm_name=config["model"]["atm_name"],
              grd_temp=temp_0)  # config["model"]["grd_temp"])
    # Create file tables.inp
    CookTables(save_path=dir_path,
               print_ids=config["tables"]["print"],
               export_ids=config["tables"]["export"])
    # Create file task.inp
    CookAiresINP(task_name=dir_name, save_path=dir_path)

    # Execute Aires
    os.system(f"cd {dir_path}; Aires < {dir_name}.inp")  # It Works

    # Execute gfortran for uncompress .grdpcles data from bash
    os.system(f"cd {dir_path}; "
              "gfortran -o grdpcles_map ../../grdpcles_reader.f -L${HOME}"
              f"/aires/{config['AiresVersion']}/lib/ -lAires -lgfortran")
    os.system(f"cd {dir_path}; "
              "./grdpcles_map << XX1\n"
              f"{dir_name}.grdpcles\n"  # Input file
              f"{dir_name}.dat\n"       # Output file
              "10000. 10000.\n"         # Size of grid x and y (m)
              "25.\n"                   # Step (m)
              "5\n"                     # Number of showers
              "XX1")
    if config["SRY_dir"]:  # Copy any taskname.sry to ROOT_DIR/SUMMARY/
        os.system(f"cd {dir_path};"
                  f"cp {dir_name}.sry {sry_full_path}")

    # Save angles data on ./angles_distribution.txt
    gamma_hist, elect_hist, muons_hist = grdpcles_dat(dir_path=dir_path, dir_name=dir_name, save_plots=True, deg=True)
    row = np.hstack((gamma_hist, elect_hist, muons_hist))
    hits_by_angle = np.vstack((hits_by_angle, row))
    # break  # Works Only for First Simulation

np.savetxt(fname="angles_distribution.txt", X=hits_by_angle, fmt='%04d')

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
    # For any task:
    call_merger(muons)  # muons(+) and muons(-)
    call_merger(trons)  # positrons(+) and electrons(-)
    # are merged.
