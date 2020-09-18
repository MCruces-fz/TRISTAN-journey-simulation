# shipTristanPT
 Simulation of particle showers on the TRISTAN detector on its journey 
 through the Atlantic Ocean.
 
## Usage:
The user only must configure the settings table with her/his preferences, 
which is the *config.json* file, and bring the *HeightDensData.txt* file 
inside ROOT_DIR. Then, executing *main.py*, the AiresINP and OUTPUT directories 
will be created.

### Auto generated directories:
- ***AiresINP***: here are generated folders with one simulation 
each one like those ones:
    + ***18364-0000***: Year 2019, Day Of the Year 364, Time 0h 00 mins
        * *18364-0000.inp*: Aires INPut file.
        * *tables.inp*: Aires file which specifies tables to print and export.
        * *model.inp*: Aires file which specifies atmospheric model.
        * *18364-0000.tnnnn*: Aires tables generated (nnnn is the code of the 
        table, which is specified by user in config.json > tables > print/ export.
        All the codes are explained on Aires Users Guide).
        * *18364-0000.sry*: Aires summary of the simulation.
        * ... Other files explained on the Aires Users Guide.
    + 18365-0600: Year 2019, Day Of the Year 364, Time 6h 00 mins
        * ...
    + ...
- ***OUTPUT***: here are stored the output histograms

## Files:
- *main.py*: main file which manages all functionalities.
- *update_aires_input.py*, *update_model.py*, *update_tables.py*: 
python files which classes; CookAiresINP, CookModel, CookTables; 
that create the main aires input file and attachments like 
*model.inp* and *tables.inp*, respectively.
- *represent.py*: there are three classes within it defined
- *HeightDensData.txt*: Input file with the data for every simulation: one
simulation for each line.
- *config.json*: **settings** table for user.
    + model: (string values)
        * atm_ident: identifier for the atmospheric model created.
        * atm_name: extended name for the atmospheric model.
        * grd_temp: temperature at background in K.
    + tables: (integer values)
        * print: list with codes for tables to print.
        * export: list with codes for tables to export.
    + template:
        * total_showers: (int)
        * primary_particle: (str)
        * primary_energy: (str)
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