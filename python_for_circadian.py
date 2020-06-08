""
==========
Author: Tomoki WATANABE
Update: 01/05/2020
Version: 2.0
License: BSD License
Programing Language: Python3
==========
"""
import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.fftpack import fft



def visualizer(
    file_name, # WITHOUT file extention. E.g. sample.csv -> sample
    file_path = '', # E.g. C:\Users\Data\sample.csv -> C:\Users\Data\
    file_from = 2, # If it comes from LUMICEC -> 0, otherwise 2. Default 2.
    sampling_period = 60,
    estimated_period = 24,
    over_view_plot_switch = 1,
    all_plot_switch = 1,
    x_axis_title = "Time [h]",
    y_axis_title = "Bioluminescence",
    column_number = 3,
    y_axis_share_switch = 1,
    color_list = ["black", "red", "orange", "green", "lightgreen", "blue", "lightblue", "yellow", "teal", "cyan",  "gray"],
    subtitle_list = ["Group0", "Group1", "Group2", "Group3", "Group4", "Group5", "Group6", "Group7", "Group8", "Group9", "Group10"],
    # Detail settings
    ## Overview plot
    ov_length = 4.5,  # Over view plot image hight
    ov_width = 5,  # Over view plot image width
    ## All plot
    a_column = 12,  # All plot columns number
    a_length = 2.5,  # All plot image hight
    a_width = 2.5  # All plot image width
    ):


    def color_changer(data_number):
        COLOR = color_list[int(data_number)]
        Subtitle = subtitle_list[int(data_number)]
        return COLOR, Subtitle


    def well_namer(i):
        if  i <= 12:
            ROW = 'A'
            COLUMN = i
        elif i <= 24 :
            ROW = 'B'
            COLUMN = i-12
        elif i <=36 :
            ROW = 'C'
            COLUMN = i-24
        elif  i <= 48:
            ROW = 'D'
            COLUMN = i-36
        elif i <= 60 :
            ROW = 'E'
            COLUMN = i-48
        elif i <=72 :
            ROW = 'F'
            COLUMN = i-60
        elif  i <= 84:
            ROW = 'G'
            COLUMN = i-72
        else :
            ROW = 'H'
            COLUMN = i-84

        if COLUMN <= 9:
            Col = '0{}'.format(COLUMN)
        else :
            Col = COLUMN

        return ROW, Col


    def router():
        raw_data = pd.read_csv("{0}{1}.csv".format(file_path, file_name), engine="python", encoding="utf-8_sig")
        try:
            new_data = raw_data.drop('Unnamed: 0', axis=1).T
            X_axis = round(raw_data["Unnamed: 0"].iloc[1:].reset_index(drop=True).astype(float), 4)
        except KeyError:
            new_data = raw_data.drop('Time', axis=1).T
            X_axis = round(raw_data['Time'].iloc[1:].reset_index(drop=True).astype(float), 4)
        finally:
            try:
                all_data = new_data.drop(0, axis=1).T.reset_index(drop=True)
                data_name = file_name
            except:
                print("<==========\nCSV file Error. \n\nA1 cell needs to be 'Time' or blank.\n==========>")
                sys.exit()
            else:
                if y_axis_share_switch == 0:
                    Yaxis = "Not shared"
                else :
                    Yaxis = "Y shared"

                if over_view_plot_switch == 1:
                    colored_overview_n_columns(X_axis, new_data, all_data, data_name, Yaxis, column_number)
                else:
                    pass

                if all_plot_switch == 1:
                    all_plot(X_axis, new_data, all_data, data_name, Yaxis)
                else:
                    pass


    def colored_overview_n_columns(X_axis, new_data, all_data, data_name, Yaxis, n):
        group_list = sorted(list(set(new_data[0])))

        F_max = np.amax(np.amax(all_data))
        Y_max = -(-F_max//1000)*1000

        fig = plt.figure(figsize=(n*ov_width, -(-(len(group_list)+n)//n)*ov_length))
        for I in range (0, len(group_list)+1, 1):
            if n <= 1:
                ax =  fig.add_subplot(-(-(len(group_list)+n)//n), n, I+1)
            else :
                if I < 1:
                    ax =  fig.add_subplot(-(-(len(group_list)+n)//n), n, I+1)
                else:
                    ax =  fig.add_subplot(-(-(len(group_list)+n)//n), n, I + n)

            if I == 0:
                process_data = all_data
                name = 'ALL'
                color_number = "-"
                plot_line_list = []
                for i in range(0, len(group_list)):
                    plot_line = ax.plot(X_axis, new_data[new_data[0]==group_list[i]].drop(0, axis=1).T.reset_index(drop=True), color='{}'.format(color_list[int(group_list[i])]), label=subtitle_list[int(group_list[i])])
                    plot_line_list.append(plot_line[0])
                ax.legend(plot_line_list, plot_line_list)
            else :
                process_data = new_data[new_data[0]==group_list[I-1]].drop(0, axis=1).T.reset_index(drop=True)
                name = subtitle_list[int(group_list[I-1])]
                color_number = "No.{}".format(round(group_list[I-1]))
                ax.plot(X_axis, process_data, color='{}'.format(color_list[round(group_list[I-1])]))

            data_time_lenght = len(process_data)
            n_rythm = int(-(-(data_time_lenght/(60/sampling_period))//24))
            X_max = int(n_rythm*24)
            original_lenght = len(all_data.T)
            data_lenght = len(process_data.T)
            data_percentage = round(data_lenght/original_lenght*100, 1)

            each_title = '{0} - {1} ({2}), {3}well ({4}%)'.format(data_name, name, color_number, data_lenght, data_percentage)
            ax.set_title(each_title)
            ax.set_xticks(np.linspace(0, X_max, n_rythm+1))
            ax.set_xticks(np.linspace(0, X_max, n_rythm*4+1), minor=True)
            ax.set_xlabel(x_axis_title)
            if Yaxis == "Y shared":
                ax.set_ylim(0, Y_max)
            ax.set_ylabel(y_axis_title)
            ax.grid(axis="both")

        fig.tight_layout()
        plt.savefig( "{0} - overview_{1}_col_plot.jpg".format(data_name, n))
        plt.show()


    def all_plot(X_axis, new_data, all_data, data_name, Yaxis):
        F_max = np.amax(np.amax(new_data))
        Y_max = -(-F_max//1000)*1000
        fig = plt.figure(figsize=(a_column*a_width, -(-new_data.shape[0]//a_column)*a_length))
        print("file_from : {}".format(file_from))
        for i in range(1, new_data.shape[0]+1):
            ax =  fig.add_subplot(-(-new_data.shape[0]//a_column),a_column,i)

            if file_from == 0:
                ROW, Col = well_namer(i)
                Name = '{0}{1}'.format(ROW, Col)
            else :
                Name = new_data.index[i-1]

            try:
                show = new_data.T[Name]
            except KeyError:
                ax.set_title("No Data")
                continue

            try:
                COLOR, Subtitle = color_changer(show[0])
            except:
                ax.set_title("No Data")
                continue

            Shaped_data = show.drop(0, axis=0).reset_index(drop=True)
            data_time_lenght = len(Shaped_data)
            n_rythm = int(-(-(data_time_lenght/(60/sampling_period))//24))
            X_max = int(n_rythm*24)

            ax.plot(X_axis, Shaped_data, color='{}'.format(COLOR))
            ax.set_title('{0} ({1})'.format(Name, Subtitle))
            ax.set_xticks(np.linspace(0, X_max, n_rythm+1))
            ax.set_xticks(np.linspace(0, X_max, n_rythm*4+1), minor=True)

            if Yaxis == "Y shared":
                function = ax.set_ylim(0, Y_max)
                Title = data_name + '-96well Plot (Y axis shared)'
            else :
                function = "#"
                Title = data_name + '-96well Plot (Y axis NOT shared)'
            function
            ax.grid(axis="both")

        fig.tight_layout()
        fig.suptitle(Title, fontsize=25)
        plt.subplots_adjust(top=0.95, left=0.05, bottom=0.08)
        fig.text(0.5, 0.02, x_axis_title, ha='center', va='center', fontsize=15)
        fig.text(0.02, 0.5, y_axis_title, ha='center', va='center', rotation='vertical', fontsize=15)
        fig.align_labels()
        image_name = data_name
        plt.savefig( "{} - All_plot.jpg".format(data_name))
        plt.show()

    router()
