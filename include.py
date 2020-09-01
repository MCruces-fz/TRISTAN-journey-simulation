# with open('model.inp', 'w+') as f:
#     lin = f.readlines()
#     lines = list(map(lambda s: s.strip(), lin))
#     for line in lines:
#         print(line)

"""
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

atmIdent = "MyModelIDStr"
atmName = "My atmospheric model"
grdTemp = 300

hList = [0, 0.8, 4, 12, 35, 100]  # km
hUnits = []
for h in hList:
    if h < 1:
        hu = [h * 1000, "m"]
    else:
        hu = [h, "km"]
    hUnits.append(hu)

densList = ["MatchDefault", 1.2184, 0.8422, 0.2765, 6.4846E-9, "MatchDefault"]  # kg/m3
densUnits = []
for d in densList:
    if type(d) == str:
        du = [d, ""]
        densUnits.append(du)
        continue
    if d < 10E-3:
        du = [d * 1000, "g/cm3"]
    else:
        du = [d, "kg/m3"]
    densUnits.append(du)

addLayer = ""
for idx in range(len(hUnits) - 1):
    hi, hui = hUnits[idx]
    di, dui = densUnits[idx]
    hf, huf = hUnits[idx + 1]
    df, duf = densUnits[idx + 1]
    addLayer += f"  AddLayer\t{hi} {hui}\t{hf} {huf}\t{di} {dui}\t{df} {duf}"
    addLayer += "\n"

atmosModel = f"""
AddAtmosModel &gammalabel
  AtmIdent {atmIdent}
  AtmName {atmName}
  AtmDefault GAMMA GrdTemp {grdTemp} K
{addLayer}
&gammalabel
"""

with open('model.inp', 'w+') as f:
    f.write(atmosModel)
