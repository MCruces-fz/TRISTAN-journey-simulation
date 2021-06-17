"""
Author: Miguel Cruces
e-mails:
- miguel.cruces.fernandez@usc.es
- mcsquared.fz@gmail.com
"""

import json
import os
from os.path import join as join_path

# Root Directory of the Project
ROOT_DIR = os.path.abspath("./")


class CookTables:
    def __init__(self, print_ids: list = None, export_ids: list = None, save_path=None):
        # self.table_ids = {
        #     "electron": 2505,
        #     "muon+": 2507,
        #     "muon-": 2508,
        #     "gamma": 2501
        # }
        if print_ids is None:
            print_ids = [2501, 2505, 2507, 2508]
        if export_ids is None:
            export_ids = [2501, 2505, 2507, 2508]

        print_tables = self.set_print(print_ids)
        export_tables = self.set_export(export_ids)

        self.input_tables = self.set_tables(print_tables, export_tables)
        self.save_tables(save_path)

    @staticmethod
    def set_export(chosen_tables):
        export_tables = ""
        for table in chosen_tables:
            export_tables += f"ExportTable {table}\n"
        return export_tables

    @staticmethod
    def set_print(chosen_tables):
        print_tables = ""
        for table in chosen_tables:
            # print_tables += f"PrintTable {self.table_ids[table]}    # {table}\n"  # With table name
            print_tables += f"PrintTable {table}\n"
        return print_tables

    @staticmethod
    def set_tables(print_tables, export_tables):
        text_tables = "#------------------------------------------------------------------------------\n" \
                      "#\n" \
                      "# File tables.inp: Input file included from travel_TT.inp\n" \
                      "#\n" \
                      "#------------------------------------------------------------------------------\n" \
                      "\n" \
                      "#------------------------ OUTPUT CONTROL STATEMENTS ---------------------------\n" \
                      "\n" \
                      "# LaTeX  # To print with better appearance\n" \
                      "StackInfo  # To see stack usage (rather technical stuff).\n" \
                      "OutputListing Full  # More technical stuff.\n" \
                      "TableIndex # Use this directive once, hard copy the resulting listing and\n" \
                      "           # keep it at hand. It is useful for reference.\n" \
                      "\n" \
                      "#---------------------- ENERGY DISTRIBUTION AT GROUND -------------------------\n" \
                      "\n" \
                      f"{print_tables}" \
                      "\n" \
                      f"{export_tables}" \
                      "\n" \
                      "ELimsTables 1 MeV 1 TeV"
        return text_tables

    def save_tables(self, save_path):
        if save_path is not None:
            save_in = save_path
        else:
            save_in = ROOT_DIR
        with open(join_path(save_in, 'tables.inp'), 'w+') as f:
            f.write(self.input_tables)


if __name__ == "__main__":
    CookTables()
