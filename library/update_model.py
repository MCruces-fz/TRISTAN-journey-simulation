"""
Author: Miguel Cruces
e-mails:
- miguel.cruces.fernandez@usc.es
- mcsquared.fz@gmail.com

    In this code, class CookModel generates a string like this:

AddAtmosModel &mylabel
  AtmIdent MyModelIDStr
  AtmName My atmospheric model
  AtmDefault GAMMA GrdTemp 300 K
  AddLayer	0 m	800 m	MatchDefault	1.2184 kg/m3
  AddLayer	800 m	4 km	1.2184 kg/m3	0.8422 kg/m3
  AddLayer	4 km	12 km	0.8422 kg/m3	0.2765 kg/m3
  AddLayer	12 km	35 km	0.2765 kg/m3	6.4846E-6 g/cm3
  AddLayer	35 km	100 km	6.4846E-6 g/cm3 MatchDefault
&mylabel
"""

import json
import os
from os.path import join as join_path

from utils.constants import ROOT_DIR


class CookModel:
    def __init__(self, atm_ident: str = "MyModelIDStr",
                 input_df_row=None,
                 atm_name: str = "My atmospheric model",
                 grd_temp: int = 300,
                 save_path=None):

        with open("utils/config.json", "r") as config_file:
            configuration = json.load(config_file)
        self.config = configuration

        h_list = [0, 0.8, 4, 12, 35, 100]  # km
        self.h_units = self.set_height_units(h_list)

        if input_df_row is None:
            dens_list = ["MatchDefault   ", 1.2184, 0.8422, 0.2765, 6.4846E-9, "MatchDefault   "]  # kg/m3
        else:
            dens_list = self.set_dens_list(input_df_row)

        self.dens_units = self.set_dens_units(dens_list)

        self.layers = self.add_layers()
        self.atmos_model = self.set_model(atm_ident, atm_name, grd_temp)

        self.save_model(save_path)

    @staticmethod
    def set_height_units(h_list):
        h_units = []
        for h in h_list:
            if h < 1:
                hu = [h * 1000, "m"]
            else:
                hu = [h, "km"]
            h_units.append(hu)
        return h_units

    @staticmethod
    def set_dens_list(inp_df):
        d_list = ["MatchDefault   ",
                  inp_df["Dens-1"],
                  inp_df["Dens-2"],
                  inp_df["Dens-3"],
                  inp_df["Dens-4"],
                  "MatchDefault   "]  # kg/m3
        # print(f"dlist= {d_list}")
        return d_list

    @staticmethod
    def set_dens_units(dens_list):
        dens_units = []
        for d in dens_list:
            if type(d) == str:
                du = [d, ""]
                dens_units.append(du)
                continue
            if d <= 1E-3:
                du = [d * 1E3, "g/cm3"]
            # if 1E-6 < d <= 1E-3:
            #     du = [d * 1E3, "g/cm3"]
            # elif d <= 1E-6:
            #     du = [d * 1E6, "kg/cm3"]
            # elif 1E-12 < d <= 1E-9:
            #     du = [d * 1E9, "kg/cm3"]  # Not accepted by aires
            else:
                du = [d, "kg/m3"]
            dens_units.append(du)
        return dens_units

    def add_layers(self):
        layers = ""
        for idx in range(len(self.h_units) - 1):
            hi, hui = self.h_units[idx]  # Height initial value and Height initial Units
            di, dui = self.dens_units[idx]  # Density initial value and density initial values
            hf, huf = self.h_units[idx + 1]  # Height final value and Height final Units
            df, duf = self.dens_units[idx + 1]  # Density final value and density final values
            try:
                layers += f"  AddLayer\t{hi:.0f} {hui} \t{hf:.0f} {huf}\t{di:.5e} {dui}\t{df:.5e} {duf}"
            except ValueError:
                try:
                    layers += f"  AddLayer\t{hi:.0f} {hui} \t{hf:.0f} {huf}\t{di} {dui}\t{df:.5e} {duf}"
                except ValueError:
                    layers += f"  AddLayer\t{hi:.0f} {hui} \t{hf:.0f} {huf}\t{di:.5e} {dui}\t{df} {duf}"
            layers += "\n"
        return layers

    def set_model(self, atm_ident, atm_name, grd_temp):
        atmos_model = f"AddAtmosModel &gamma_label\n" \
                      f"  AtmIdent {atm_ident}\n" \
                      f"  AtmName {atm_name}\n" \
                      f"  AtmDefault GAMMA GrdTemp {grd_temp} K\n" \
                      f"{self.layers}" \
                      f"&gamma_label\n" \
                      f"Atmosphere {atm_ident}"
        return atmos_model

    def save_model(self, save_path):
        if save_path is not None:
            save_in = save_path
        else:
            save_in = ROOT_DIR
        with open(join_path(save_in, 'model.inp'), 'w+') as f:
            f.write(self.atmos_model)


if __name__ == "__main__":
    import pandas as pd
    inpt_df = pd.read_csv("../TRISTAN_data_000.txt", index_col=0, header=0, delim_whitespace=True, na_values="(missing)")
    for row in inpt_df.iterrows():
        CookModel(input_df_row=row[1], save_path="/home/mcruces/Downloads")
        break
