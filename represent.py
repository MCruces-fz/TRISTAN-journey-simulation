import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import os
from os.path import join as join_path

# Root Directory of the Project
ROOT_DIR = os.path.abspath("./")


def grdpcles_dat(dir_path: str, dir_name: str, save_plots: bool = False, deg: bool = True):
    """
    It makes an histogram with the number of particles of each type (gammas, electrons,
    mouns) with bins equiseparated from each other by 5 degrees

    :param dir_path: path to the directory with the archive.dat
    :param dir_name: name of the archive.dat
    :param save_plots: True if save, False if not.
    :param deg: True in degrees, False in radians.
    :return: Three arrays (gammas, electrons, mouns) with number of particles in each bin.
    """
    plt.close("all")

    save_path = join_path(ROOT_DIR, "OUTPUT")
    full_path_name = join_path(dir_path, dir_name)

    with open(f"{full_path_name}.dat", newline='\n') as f:
        raw_lines = f.readlines()
        # print("*** Len Data: ", len(raw_lines))
        data = np.zeros((0, 6))
        count = 0
        for line in raw_lines:
            count += 1
            # print(count, "/", len(raw_lines))
            row = [float(i) for i in line.split()]
            data = np.vstack((data, row))

    ux = data[:, 3]
    uy = data[:, 4]
    kin_e = data[:, 5]
    uz = - np.sqrt(1 - ux ** 2 - uy ** 2)
    angle = np.arctan(- np.sqrt(ux ** 2 + uy ** 2) / uz)

    r = data[:, 1]
    phi = data[:, 2]
    '''
    plt.figure('Positions')
    # plt.plot(r * np.cos(phi), r * np.sin(phi))
    plt.plot(r * np.cos(phi), r * np.sin(phi), "k.")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Position Hits at Ground')
    if save_plots:
        plt.savefig(f'{save_path}/{dir_name}_positions.png')
    '''

    fig, ax = plt.subplots(ncols=1, figsize=(7, 4))
    hb = ax.hexbin(r, phi, bins='log', cmap='jet')  # TODO: change to hist2d
    ax.set_title("Hexagon coordinates")
    ax.set_xlabel('Distance from core / m')
    ax.set_ylabel('Polar angle / rad')
    cb = fig.colorbar(hb, ax=ax)
    cb.set_label('counts')
    if save_plots:
        fig.savefig(f'{save_path}/{dir_name}_phi_r_coordinates.png')

    fig, ax = plt.subplots(ncols=1, figsize=(7, 4))
    hb = ax.hexbin(phi, kin_e, bins='log', cmap='jet')  # TODO: change to hist2d
    ax.set_title("Hexagon energies")
    ax.set_xlabel('Polar angle / rad')
    ax.set_ylabel('Particle Energy / GeV')
    cb = fig.colorbar(hb, ax=ax)
    cb.set_label('counts')
    if save_plots:
        fig.savefig(f'{save_path}/{dir_name}_E_phi_coordinates.png')

    codes = data[:, 0]
    gamm_ids = np.where(codes == 1)
    elec_ids = np.where(abs(codes) == 2)
    muon_ids = np.where(abs(codes) == 3)

    deg_bins = np.array([0., 5., 10., 15., 20., 25., 30., 35., 40., 45.,
                         50., 55., 60., 65., 70., 75., 80., 85., 90., 95.])
    rad_bins = deg_bins * np.pi / 180.

    plt.figure('Gammas')
    if deg:
        gamma_hist, _, _ = plt.hist(angle[gamm_ids] * 180. / np.pi, bins=deg_bins)
        plt.xlabel('Zenith Angle / deg')
    else:
        gamma_hist, _, _ = plt.hist(angle[gamm_ids], bins=rad_bins)
        plt.xlabel('Zenith Angle / rad')
    plt.ylabel('Number of gammas at grid')
    # plt.xlim(0, 1.6)
    # plt.ylim(0, 1400)
    plt.title('Gammas Histogram')
    if save_plots:
        plt.savefig(f'{save_path}/{dir_name}_gammas_histogram.png')

    plt.figure('Electrons')
    if deg:
        elect_hist, _, _ = plt.hist(angle[elec_ids] * 180. / np.pi, bins=deg_bins)
        plt.xlabel('Zenith Angle / deg')
    else:
        elect_hist, _, _ = plt.hist(angle[elec_ids], bins=rad_bins)
        plt.xlabel('Zenith Angle / rad')
    plt.ylabel('Number of electrons at grid')
    # plt.xlim(0, 1.6)
    # plt.ylim(0, 1400)
    plt.title('Electrons Histogram')
    if save_plots:
        plt.savefig(f'{save_path}/{dir_name}_electrons_histogram.png')

    plt.figure('Muons')
    if deg:
        muons_hist, _, _ = plt.hist(angle[muon_ids] * 180. / np.pi, bins=deg_bins)
        plt.xlabel('Zenith Angle / deg')
    else:
        muons_hist, _, _ = plt.hist(angle[muon_ids], bins=rad_bins)
        plt.xlabel('Zenith Angle / rad')
    plt.ylabel('Number of muons at grid')
    # plt.xlim(0, 1.6)
    # plt.ylim(0, 1400)
    plt.title('Muons Histogram')
    if save_plots:
        plt.savefig(f'{save_path}/{dir_name}_muons_histogram.png')

    plt.figure('All Part')
    if deg:
        plt.hist(angle * 180. / np.pi, bins=deg_bins)
        plt.xlabel('Polar Angle / deg')
    else:
        plt.hist(angle, bins=rad_bins)
        plt.xlabel('Polar Angle / rad')
    plt.ylabel('Number of particles at grid')
    # plt.xlim(0, 1.6)
    # plt.ylim(0, 1400)
    plt.title('Particles Histogram')
    if save_plots:
        plt.savefig(f'{save_path}/{dir_name}_all_particles_histogram.png')

    plt.close("all")
    return gamma_hist, elect_hist, muons_hist


if __name__ == "__main__":
    grdpcles_dat(dir_path=join_path(ROOT_DIR, join_path("AiresINP", "18350-0000")),
                 dir_name="18350-0000", save_plots=True, deg=True)


class CookingDataAIRES:
    def __init__(self, in_path: str = "./", file: str = 'learn1.t2505', e_units="MeV"):
        """
        Class which reads data from table files.tnnnn exported by AIRES and manages it.

        :param in_path: Absolute path to file directory
        :param file: Name (with extension) of the file.tnnnn
        :param e_units: Energy Units to convert all data (AIRES format)
        """
        # Initialize constants
        self.file_name = file
        self.table_name = ''
        self.units = {}
        self.date = None
        self.num_showers = 0
        self.col_titles = []
        self.data_frame = None

        # Invoke functions
        self.read_data(in_path)
        self.energy_units(_to=e_units)

    def read_data(self, in_path):
        """
        Method which reads data from file and sotores it in a pandas dataframe

        :param in_path: Absolute path to file directory
        :return: Void function (it doesn't return anything, but it calculates dataframe)
        """
        with open(join_path(in_path, self.file_name), 'r') as f:
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
        """
        Method which changes units from dataframe

        :param _to: Unit to change
        :return: Void function (It only modifies the pandas dataframe)
        """
        unit_values = {'eV': 1, 'keV': 1e3, 'MeV': 1e6,
                       'GeV': 1e9, 'TeV': 1e12, 'PeV': 1e15}
        _from = self.units['Energy']
        factor = unit_values[_from] / unit_values[_to]
        try:
            self.data_frame['Energy'] = factor * self.data_frame['Energy']
            self.units['Energy'] = _to
        except KeyError:
            print(f"Energy has not been changed to {_to}, it is still in {_from} ({self.file_name})")


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
    def __init__(self, cook, out_path="./", task_name="task"):
        # Initialize constants
        # self.file_name = cook.file_name
        self.table_name = cook.table_name
        self.units = cook.units
        # self.date = cook.date
        # self.num_showers = cook.num_showers
        self.col_titles = cook.col_titles
        self.data_frame = cook.data_frame

        with open("config.json", "r") as config_file:
            configuration = json.load(config_file)
        self.config = configuration

        # Invoke functions
        self.diagram(out_path=out_path, task_name=task_name)
        # self.histogram()

    def diagram(self, out_path="./", task_name="task"):
        # global nonzero
        conf = self.config["plots"]

        table, title, particle = self.table_name.split(': ')
        fig = plt.figure(f"{table}_{task_name}")
        ax = fig.add_subplot()
        plt.title(f'{title}: {particle}')

        if conf["threshold"]:
            a = self.data_frame['Mean']
            a[a < conf["threshold"]] = 0
            nonzero = self.data_frame['Mean'].to_numpy().nonzero()

            x = np.asarray(self.data_frame['Energy'])[nonzero]
            y = np.asarray(self.data_frame['Mean'])[nonzero]
        else:
            try:
                x = self.data_frame['Energy']
            except KeyError:
                x = self.data_frame.iloc[:, 0]
            y = self.data_frame['Mean']
            nonzero = None

        # Mean
        if conf["mean"]:
            plt.plot(x, y, color='#000000', label='Mean.')
            ax.fill_between(x=x, y1=y, y2=0, color='#00B5B8', alpha=0.3)

        # Minimum and Maximum
        if conf["minimum_and_maximum"]:
            if conf["threshold"]:
                ymin = np.asarray(self.data_frame['Minimum'])[nonzero]
                ymax = np.asarray(self.data_frame['Maximum.'])[nonzero]
            else:
                ymin = self.data_frame['Minimum']
                ymax = self.data_frame['Maximum.']
            plt.plot(x, ymin, color='#74508D', alpha=0.25)
            plt.plot(x, ymax, color='#74508D', alpha=0.25)
            ax.fill_between(x=x, y1=ymin, y2=ymax, color='#74508D', alpha=0.3, label='Maximum and Minimum.')

        # Std. Dev.
        if conf["standard_deviation"]:
            if conf["threshold"]:
                ystd = np.asarray(self.data_frame['Std. Dev.'])[nonzero] / 2
            else:
                ystd = self.data_frame['Std. Dev.'] / 2
            plt.plot(x, y - ystd, color='#ED177A', alpha=0.5)
            plt.plot(x, y + ystd, color='#ED177A', alpha=0.5)
            ax.fill_between(x=x, y1=y - ystd, y2=y + ystd, color='#ED177A', alpha=0.2, label='Std. Dev.')

        # RMS Error.
        if conf["RMS_error"]:
            if conf["threshold"]:
                yrms = np.asarray(self.data_frame['RMS Error'])[nonzero] / 2
            else:
                yrms = self.data_frame['RMS Error'] / 2
            plt.plot(x, y - yrms, color='#279F00', alpha=0.5)
            plt.plot(x, y + yrms, color='#279F00', alpha=0.5)
            ax.fill_between(x=x, y1=y - yrms, y2=y + yrms, color='#279F00', alpha=0.2, label='RMS Error')

        # Config
        if self.data_frame.columns[0] == "Energy":
            ax.set_xscale('log')
            unit = self.units["Energy"]
        elif self.data_frame.columns[0] == "R (distance to the core)":
            unit = self.units["Length"]
        elif self.data_frame.columns[0] == "Depth of obs. level":
            unit = self.units["Depth"]
        else:
            unit = "#"
        ax.set_xlabel(f'{self.data_frame.columns[0]} / {unit}')
        ax.set_ylabel('Particles')
        plt.yticks(rotation=60)
        ax.legend(loc='best')
        ax.grid(which='both', alpha=0.25)

        if conf["save_plots"]:
            fig.savefig(join_path(out_path,
                                  f"{table.replace(' ', '_')}_"
                                  f"{title.replace(' ', '_')}_"
                                  f"{particle.replace(' ', '_')}_"
                                  f"{task_name}.png"))

        if conf["show_plots"]:
            plt.show()
        else:
            plt.close("all")

    def histogram(self):
        table, title, particle = self.table_name.split(':')
        fig = plt.figure(table)
        ax = fig.add_subplot()
        plt.title(f'{title}: {particle}')
        x = self.data_frame['Energy']
        ax.hist(x, bins='auto')


if __name__ == '__main__':
    input_path = "/home/mcruces/Documents/GitHub/TRISTAN-journey-PT/AiresINP/18350-0000/"
    # input_path = "/home/mcruces/Documents/GitHub/CodeBlocks/AIRES/"
    file_name = "18350-0000"
    # file_name = "learn1"
    gamma = CookingDataAIRES(in_path=input_path, file=f'{file_name}.t2501')
    elect = CookingDataAIRES(in_path=input_path, file=f'{file_name}.t2505')
    p_muon = CookingDataAIRES(in_path=input_path, file=f'{file_name}.t2507')
    m_muon = CookingDataAIRES(in_path=input_path, file=f'{file_name}.t2508')

    muons = MergeData(p_muon, m_muon)
    output = muons.data_frame

    Represent(gamma)
    Represent(elect)
    Represent(muons)
