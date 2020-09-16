# shipTristanPT
 Simulation of particle showers on the TRISTAN detector on its journey 
 through the Atlantic Ocean.

## Files:
- *main.py*: main file which manages all functionalities.
- *update_aires_input.py*, *update_model.py*, *update_tables.py*: 
python files which classes; CookAiresINP, CookModel, CookTables; 
that create the main aires input file and attachments like 
*model.inp* and *tables.inp*, respectively.
- *represent.py*: there are three classes within it defined
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

## Auto generated directories:
- ***AiresINP***: here are generated folders with one simulation 
each one.
- ***OUTPUT***: here are stored the output histograms