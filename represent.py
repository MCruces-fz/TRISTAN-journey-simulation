import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class CookingDataAIRES:
    def __init__(self, file: str = 'learn1.t2505'):
        # Initialize constants
        self.file_name = file
        self.table_name = ''
        self.units = {}
        self.date = None
        self.num_showers = 0
        self.col_titles = []
        self.data_frame = None

        # Invoke functions
        self.read_data()
        self.energy_units(_to='MeV')

    def read_data(self):
        with open(self.file_name, 'r') as f:
            lin = f.readlines()
            lines = list(map(lambda s: s.strip(), lin))
            data = []
            for idx, line in enumerate(lines):
                if line[0] == '#':
                    if 'Task starting date:' in line:
                        self.date = line.split('date: ')[1]
                    if 'Number of showers' in line:
                        self.num_showers = int(line[-5:])
                    if 'TABLE' in line:
                        self.table_name = line.replace('#   ', '').replace('.', '')
                    if 'Units used' in line:
                        ix = idx + 2
                        newline = lines[ix]
                        while '# ' in newline:
                            magnitude, unit = newline.replace('#', '').replace(' ', '').split('---')
                            self.units[magnitude] = unit
                            ix += 1
                            newline = lines[ix]
                    if 'Columns' in line:
                        ix = idx + 2
                        newline = lines[ix]
                        title_str = ''
                        while '# ' in newline:
                            title_str += newline.replace('#         ', '').replace(', ', ',')
                            ix += 1
                            newline = lines[ix]
                        titles = title_str.split(',')
                        for tit in titles:
                            self.col_titles.append(tit[2:])
                else:
                    data.append(np.asarray(line.split(), dtype=np.float))

            dat_array = np.asarray(data)
            self.data_frame = pd.DataFrame(data=dat_array[:, 1:],
                                           index=dat_array[:, 0].astype(np.int),
                                           columns=self.col_titles[1:])

    def energy_units(self, _to='MeV'):
        unit_values = {'eV': 1, 'keV': 1e3, 'MeV': 1e6,
                       'GeV': 1e9, 'TeV': 1e12, 'PeV': 1e15}
        _from = self.units['Energy']
        factor = unit_values[_from] / unit_values[_to]
        self.data_frame['Energy'] = factor * self.data_frame['Energy']
        self.units['Energy'] = _to


class MergeData:
    def __init__(self, cook_a, cook_b):
        # Initialize constants

        table_a, title_a, particle_a = cook_a.table_name.split(': ')
        table_b, title_b, particle_b = cook_b.table_name.split(': ')
        self.table_name = f'TABLES {table_a[-4:]} {table_b[-4:]}: {title_a}: {particle_a} and {particle_b}'

        if cook_a.units == cook_b.units:
            self.units = cook_a.units
        else:
            raise Exception('You are trying to sum values with different units.')

        if cook_a.col_titles == cook_b.col_titles:
            self.col_titles = cook_a.col_titles
        else:
            raise Exception('You are trying to merge data frames with different columns.')

        self.data_frame_a = cook_a.data_frame
        self.data_frame_b = cook_b.data_frame

        self.data_frame = self.merge()

    def merge(self):
        out_data_frame = self.data_frame_a.copy()
        out_data_frame.iloc[:, 1:] = self.data_frame_a.iloc[:, 1:].add(self.data_frame_b.iloc[:, 1:], axis='columns')
        return out_data_frame


class Represent:
    def __init__(self, cook):
        # Initialize constants
        # self.file_name = cook.file_name
        self.table_name = cook.table_name
        self.units = cook.units
        # self.date = cook.date
        # self.num_showers = cook.num_showers
        self.col_titles = cook.col_titles
        self.data_frame = cook.data_frame

        # Invoke functions
        self.diagram()
        # self.histogram()

    def diagram(self):
        table, title, particle = self.table_name.split(': ')
        fig = plt.figure(table)
        ax = fig.add_subplot()
        plt.title(f'{title}: {particle}')

        x = self.data_frame['Energy']

        # Mean
        y = self.data_frame['Mean']
        plt.plot(x, y, color='#000000', label='Particles at Ground.')
        ax.fill_between(x=x, y1=y, y2=0, color='#00B5B8', alpha=0.3)

        # Minimum and Maximum
        # ymin = self.data_frame['Minimum']
        # ymax = self.data_frame['Maximum.']
        # plt.plot(x, ymin, color='#74508D', alpha=0.25)
        # plt.plot(x, ymax, color='#74508D', alpha=0.25)
        # ax.fill_between(x=x, y1=ymin, y2=ymax, color='#74508D', alpha=0.3, label='Maximum and Minimum.')

        # Std. Dev.
        ystd = self.data_frame['Std. Dev.'] / 2
        plt.plot(x, y - ystd, color='#ED177A', alpha=0.5)
        plt.plot(x, y + ystd, color='#ED177A', alpha=0.5)
        ax.fill_between(x=x, y1=y - ystd, y2=y + ystd, color='#ED177A', alpha=0.2, label='Std. Dev.')

        # RMS Error.
        yrms = self.data_frame['RMS Error'] / 2
        plt.plot(x, y - yrms, color='#279F00', alpha=0.5)
        plt.plot(x, y + yrms, color='#279F00', alpha=0.5)
        ax.fill_between(x=x, y1=y - yrms, y2=y + yrms, color='#279F00', alpha=0.2, label='RMS Error')

        # Config
        ax.set_xlabel(f'Energy / {self.units["Energy"]}')
        ax.set_xscale('log')
        ax.set_ylabel('Particles at Ground')
        plt.yticks(rotation=60)
        ax.legend(loc='best')
        ax.grid(which='both', alpha=0.25)

        fig.savefig(f"{table.replace(' ', '_')}_{title.replace(' ', '_')}_{particle.replace(' ', '_')}.png")

    def histogram(self):
        table, title, particle = self.table_name.split(':')
        fig = plt.figure(table)
        ax = fig.add_subplot()
        plt.title(f'{title}: {particle}')
        x = self.data_frame['Energy']
        ax.hist(x, bins='auto')


if __name__ == '__main__':
    gamma = CookingDataAIRES(file='learn1.t2501')
    elect = CookingDataAIRES(file='learn1.t2505')
    p_muon = CookingDataAIRES(file='learn1.t2507')
    m_muon = CookingDataAIRES(file='learn1.t2508')

    muons = MergeData(p_muon, m_muon)
    output = muons.data_frame

    Represent(gamma)
    Represent(elect)
    Represent(muons)
