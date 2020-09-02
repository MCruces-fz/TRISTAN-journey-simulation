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

with open("config.json", "r") as config_file:
    config = json.load(config_file)


class CookModel:
    def __init__(self, atm_ident: str = "MyModelIDStr", atm_name: str = "My atmospheric model", grd_temp: int = 300):

        h_list = [0, 0.8, 4, 12, 35, 100]  # km
        self.h_units = self.set_height_units(h_list)
        dens_list = ["MatchDefault", 1.2184, 0.8422, 0.2765, 6.4846E-9, "MatchDefault"]  # kg/m3
        self.dens_units = self.set_dens_units(dens_list)

        self.layers = self.add_layers()
        self.atmos_model = self.set_model(atm_ident, atm_name, grd_temp)

        self.save_model()

    def set_height_units(self, h_list):
        h_units = []
        for h in h_list:
            if h < 1:
                hu = [h * 1000, "m"]
            else:
                hu = [h, "km"]
            h_units.append(hu)
        return h_units

    def set_dens_units(self, dens_list):
        dens_units = []
        for d in dens_list:
            if type(d) == str:
                du = [d, ""]
                dens_units.append(du)
                continue
            if d < 10E-3:
                du = [d * 1000, "g/cm3"]
            else:
                du = [d, "kg/m3"]
            dens_units.append(du)
        return dens_units

    def add_layers(self):
        layers = ""
        for idx in range(len(self.h_units) - 1):
            hi, hui = self.h_units[idx]
            di, dui = self.dens_units[idx]
            hf, huf = self.h_units[idx + 1]
            df, duf = self.dens_units[idx + 1]
            layers += f"  AddLayer\t{hi} {hui}\t{hf} {huf}\t{di} {dui}\t{df} {duf}"
            layers += "\n"
        return layers

    def set_model(self, atm_ident, atm_name, grd_temp):
        atmos_model = f"AddAtmosModel &gamma_label\n" \
                      f"  AtmIdent {atm_ident}\n" \
                      f"  AtmName {atm_name}\n" \
                      f"  AtmDefault GAMMA GrdTemp {grd_temp} K\n" \
                      f"{self.layers}" \
                      f"&gamma_label"
        return atmos_model

    def save_model(self):
        with open('model.inp', 'w+') as f:
            f.write(self.atmos_model)


if __name__ == "__main__":
    CookModel()
