# TRISTAN Journey simulation
Simulation of particle showers on the TRISTAN detector on its journey 
through the Atlantic Ocean.

It is necessary to have installed:
 - AIRES (and added library to the `LD_LIBRARY_PATH`)
 - gfortran compiler
 - Python builtin libraries
 
## Usage:
The user only must configure the settings table with her/his preferences, 
which is the *config.json* file, and bring the *TRISTAN_data_000.txt* file 
inside `ROOT_DIR` with simulation data. Te name of input file is chosen in 
*config.json* file.

Then, executing *main.py* with Python 3, the AiresINP and OUTPUT directories 
will be created.

### Angles distribution at ground

The file ***angles_distribution.txt*** contains: number of particles which 
reach ground with azimuth angles between the next intervals:

```
|| ======== GAMMA ======== || ====== ELECTRONS ====== || ======== MUONS ======== ||
||  [0, 5], (5, 10], ...   ||  [0, 5], (5, 10], ...   ||  [0, 5], (5, 10], ...   ||
```

One line for each simulation.

### Auto generated directories:
- ***AiresINP***: here are generated folders with one simulation 
each one like those ones:
    + ***18364-0000***: Year 2018, Day Of the Year 364, Time 0h 00 mins
        * *18364-0000.inp*: Aires INPut file.
        * *tables.inp*: Aires file which specifies tables to print and export.
        * *model.inp*: Aires file which specifies atmospheric model.
        * *18364-0000.tnnnn*: Aires tables generated (nnnn is the code of the 
        table, which is specified by user in config.json > tables > print/ 
        export. All the codes are explained on Aires Users Guide).
        * *18364-0000.sry*: Aires summary of the simulation.
        * *18364-000.grdpcles*: File with large compressed data about the 
        simulation.
        * *18364-000.dat*: Chosen data uncompressed from *18364-000.grdpcles* 
        by the fortran program *grdpcles_reader.f* located in ROOT_DIR.
        * ... Other files explained on the Aires Users Guide.
    + ***18365-0600***: Year 2018, Day Of the Year 365, Time 6h 00 mins
        * *18364-0000.inp*
        * *tables.inp*
        * *model.inp*
        * *...*
    + ***...***
- ***OUTPUT***: here are stored the output histograms
- ***SUMMARY***: only generated if is set "SRY_dir": 1 in config.json. Here 
are stored all summaries, one for each simulation.

## Program files:
- *main.py*: main file which manages all functionalities.
- *update_aires_input.py*, *update_model.py*, *update_tables.py*: 
python files which classes; CookAiresINP, CookModel, CookTables; 
that create the main aires input file and attachments like 
*model.inp* and *tables.inp*, respectively.
- *represent.py*: there are three classes within it defined.
- *grdpcles_reader.f*: Program written in fortran for extracting compressed 
data from *files.grdpcles*.
- *TRISTAN_data_000.txt*: Input file with the data for every simulation: one
simulation for each line.
- *config.json*: **settings** table for user.
    + InputFileName: String with the complete name of the input file 
    *"filename.txt"*. In case it is saved in another directory, you must give 
    full path or relative path from ROOT_DIR.
    + AiresVersion: String which specifies the Aires version written in format 
    "19-04-00" (the same format as the Iroot directory for installation).
    + SRY_dir: boolean to say whether create or not the SUMMARY directory,
    where all summaries of each simulation are stored.
    + model: (string values)
        * atm_ident: identifier for the atmospheric model created.
        * atm_name: extended name for the atmospheric model.
        * grd_temp: temperature at background in K. [UNUSED]
    + tables: (list of integer values)
        * print: list with codes for tables to print.
        * export: list with codes for tables to export.
    + template:
        * total_showers: (int, It is better if it is strictly larger than 1)
        * primary_particle: (str: "neutron", "proton"... AIRES naming)
        * primary_energy: (str: "1 PeV", "100 GeV" ...)
        * oberving_levels: (int)
    + plots: say whether or not it shows the following data (boolean 
    values, but only **1** or **0**, because config.json doesn't support 
    *True* neither *False*).
        * mean:
        * minimum_and_maximum:
        * standard_deviation:
        * RMS_error:
        * show_plots:
        * save_plots:
        * threshold: Use or not threshold representing data on plots
         (0 -> Do not use threshold; 1, 2, ..., 30, 50, ..., 100, ... 
         -> Use threshold with that value.)
