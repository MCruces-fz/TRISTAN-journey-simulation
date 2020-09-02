

class CookTables:
    def __init__(self, chosen_tables: list = None):
        self.table_ids = {
            "electron": 2505,
            "muon+": 2507,
            "muon-": 2508,
            "gamma": 2501
        }
        if chosen_tables is None:
            chosen_tables = ["gamma", "electron", "muon+", "muon-"]

        print_tables = self.set_print(chosen_tables)
        export_tables = self.set_export(chosen_tables)

        self. input_tables = self.set_tables(print_tables, export_tables)
        self.save_tables()

    def set_export(self, chosen_tables):
        export_tables = ""
        for table in chosen_tables:
            export_tables += f"ExportTable {self.table_ids[table]}   # {table}\n"
        return export_tables

    def set_print(self, chosen_tables):
        print_tables = ""
        for table in chosen_tables:
            print_tables += f"PrintTable {self.table_ids[table]}    # {table}\n"
        return print_tables

    def set_tables(self, print_tables, export_tables):
        text_tables = "#------------------------------------------------------------------------------\n" \
                      "#\n" \
                      "# File tables.inp: Input file included from travel_TT.inp\n" \
                      "#\n" \
                      "#------------------------------------------------------------------------------\n" \
                      "\n" \
                      "#------------------------ OUTPUT CONTROL STATEMENTS ---------------------------\n" \
                      "\n" \
                      "LaTeX  # To print with better appearance\n" \
                      "StackInfo  # To see stack usage (rather technical stuff).\n" \
                      "OutputListing Full  # More technical stuff.\n" \
                      "TableIndex # Use this directive once, hard copy the resulting listing and\n" \
                      "           # keep it at hand. It is useful for reference.\n" \
                      "\n" \
                      "#---------------------- ENERGY DISTRIBUTION AT GROUND -------------------------\n"\
                      "\n" \
                      f"{print_tables}"\
                      "\n" \
                      f"{export_tables}"\
                      "\n" \
                      "ELimsTables 1 MeV 1 TeV"
        return text_tables

    def save_tables(self):
        with open('tables.inp', 'w+') as f:
            f.write(self.input_tables)


if __name__ == "__main__":
    CookTables()
