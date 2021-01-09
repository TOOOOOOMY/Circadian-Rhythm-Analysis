"""
==========
Author: Tomoki WATANABE
Update: 20/12/2020
Version: 4.2.2
License: BSD License
Programing Language: Python3
==========
"""
import os
import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import itertools
import json


class visualizer:
    def __init__(
        self, 
        file_name, 
        common_setting,
        subtitle_and_color,
        # compare_info
    ):

        # 96well positions 読み込み
        def well_positions_reader(file_name, file_location = "/content/"):
            # group_list = sorted(list(set(sum(positions.values.tolist(), []))))
            if os.path.exists(file_location + file_name):
                file_type = file_name.split(".")[-1]
                if file_type == "xlsx":
                    return pd.read_excel(file_location + file_name, usecols=[i for i in range(0, 13, 1)], index_col=0)[:8] #, group_list
                elif file_type == "csv":
                    return pd.read_csv(file_location + file_name, engine="python", encoding="utf-8_sig", index_col=0) # , group_list
                else :
                    print("Error : Please use xlsx or csv file.")
                    return None
            else :
                print("エラー：該当する名前の96well_position入力用ファイルが見つかりません。")
                return None

        # 測定結果読み込み
        def data_reader(file_name, file_location = "/content/"): 
            # LUMICEC出力データ読み込み
            def lumicec_reader(file_location, file_name):
                # if not file_name.split(".")[-1] == "xlsx":
                #     return print("エラー：Lumicecから取得したxlsx（エクセル）ファイルを指定してください。")
                index_rename_dict = {}
                for letter in ["A", "B", "C", "D", "E", "F", "G", "H"]:
                    for i in range(1, 13, 1):
                        index_rename_dict[letter + "列" + str(i)] = letter + (('0' + str(i)) if i <10 else str(i))
                try :
                    return pd.read_excel(
                                  file_location + "/" + file_name, 
                                  # engine="python", 
                                  # encoding="shift-jis", 
                                  # skiprows=2, 
                                  usecols=lambda x: x not in ['Time'], 
                                  sheet_name='plate1'
                                ).rename(columns=index_rename_dict)
                except Exception as e:
                    print("エラー：LUMICECデータの読み込みに失敗しました。\nシステムメッセージ：\n" + str(e))

            # ALOKA出力データ読み込み
            def aloka_reader(file_location, file_name):
                # if not file_name.split(".")[-1] == "csv":
                #    return print("エラー：Alokaから取得したcsvファイルを指定してください。")
                index_rename_dict = {}
                for letter in ["A", "B", "C", "D", "E", "F", "G", "H"]:
                    for i in range(1, 13, 1):
                        index_rename_dict[letter + "列" + str(i)] = letter + (('0' + str(i)) if i <10 else str(i))
                try :
                    return pd.read_csv(
                                  file_location + "/" + file_name, 
                                  engine="python", 
                                  encoding="shift-jis", 
                                  skiprows=2, 
                                  usecols=lambda x: x not in ['通番', '日付', '時刻', 'リピート回数']
                                ).rename(columns=index_rename_dict)
                except Exception as e:
                    print("エラー：ALOKAデータの読み込みに失敗しました。\nシステムメッセージ：\n" + str(e))
                    return None

            file_type = file_name.split(".")[-1]
            # print(file_type)
            if file_type == "csv":
                return aloka_reader(file_location, file_name)
            elif file_type == "xlsx":
                column_names = [
                                    "A01",
                                    "A02",
                                    "A03",
                                    "A04",
                                    "A05",
                                    "A06",
                                    "A07",
                                    "A08",
                                    "A09",
                                    "A10",
                                    "A11",
                                    "A12",
                                    "B01",
                                    "B02",
                                    "B03",
                                    "B04",
                                    "B05",
                                    "B06",
                                    "B07",
                                    "B08",
                                    "B09",
                                    "B10",
                                    "B11",
                                    "B12",
                                    "C01",
                                    "C02",
                                    "C03",
                                    "C04",
                                    "C05",
                                    "C06",
                                    "C07",
                                    "C08",
                                    "C09",
                                    "C10",
                                    "C11",
                                    "C12",
                                    "D01",
                                    "D02",
                                    "D03",
                                    "D04",
                                    "D05",
                                    "D06",
                                    "D07",
                                    "D08",
                                    "D09",
                                    "D10",
                                    "D11",
                                    "D12",
                                    "E01",
                                    "E02",
                                    "E03",
                                    "E04",
                                    "E05",
                                    "E06",
                                    "E07",
                                    "E08",
                                    "E09",
                                    "E10",
                                    "E11",
                                    "E12",
                                    "F01",
                                    "F02",
                                    "F03",
                                    "F04",
                                    "F05",
                                    "F06",
                                    "F07",
                                    "F08",
                                    "F09",
                                    "F10",
                                    "F11",
                                    "F12",
                                    "G01",
                                    "G02",
                                    "G03",
                                    "G04",
                                    "G05",
                                    "G06",
                                    "G07",
                                    "G08",
                                    "G09",
                                    "G10",
                                    "G11",
                                    "G12",
                                    "H01",
                                    "H02",
                                    "H03",
                                    "H04",
                                    "H05",
                                    "H06",
                                    "H07",
                                    "H08",
                                    "H09",
                                    "H10",
                                    "H11",
                                    "H12"
                                ]
                lumicec_data = lumicec_reader(file_location, file_name)
                return pd.DataFrame(
                    [lumicec_data[col_name] for col_name in column_names],
                    index = column_names,
                    columns = lumicec_data.index
                ).T
            else :
                print("Error : Please use csv or xlsx file.")
                return None

        def moving_avrg(moving_avrg_range, data):
            if moving_avrg_range < 12 or moving_avrg_range > 36:
                print("Error : moving_avrg_range should be 12 ~ 36!")
                return 
            if moving_avrg_range % 2 == 0:
                return pd.DataFrame(
                    [[value[int(moving_avrg_range/2 + i)]/(sum(value[i+1:moving_avrg_range+i])/(moving_avrg_range-1) + (value[i] + value[moving_avrg_range+i])/2) for i in range(0, len(value) - moving_avrg_range, 1)] for value in data.T.values],
                    index = data.columns.values,
                    columns = range(int(moving_avrg_range/2), len(data) - int(moving_avrg_range/2), 1)
                ).T
            else :
                return pd.DataFrame(
                    [[value[int((moving_avrg_range-1)/2 + i)]/(sum(value[i:moving_avrg_range+i])/(moving_avrg_range)) for i in range(0, len(value) - moving_avrg_range+1, 1)] for value in data.T.values],
                    index = data.columns.values,
                    columns = range(int(moving_avrg_range/2), len(data) - int(moving_avrg_range/2), 1)
                ).T

        def range_extraction(
            original_data,
            extraction_start, 
            extraction_end
            ):
            if extraction_end == 0:
                return original_data[extraction_start:]
            else :
                if extraction_start >= extraction_end:
                    print('Error : "extraction_end" should be more than "extraction_start".')
                    return None
                else :
                    return original_data[extraction_start:extraction_end + 1]

        def col_posi_linker(col_name):
            if col_name[1] == "0":
                return self.positions.at[col_name[0], col_name[2]]
            else :
                return self.positions.at[col_name[0], col_name[1:3]]

        self.file_name = file_name
        self.common_setting = common_setting
        self.subtitle_and_color = subtitle_and_color
        self.positions = well_positions_reader(common_setting["96well_position_file"])

        ranged_data = range_extraction(data_reader(file_name), common_setting["analysis_start"], common_setting["analysis_end"])

        if common_setting["yaxis_percentage_switch"]:
            def percentage_cal(data):
                new_data = pd.DataFrame(columns=data.columns.values)
                for col in data.columns.values:
                    new_data[col] = data[col]/max(data[col])*100
                return new_data
            if common_setting["moving_avrg_range"]:
                self.plot_data = percentage_cal(moving_avrg(common_setting["moving_avrg_range"], ranged_data))
            else :
                self.plot_data = percentage_cal(ranged_data)
            self.Y_max = 100
        else :
            self.plot_data = ranged_data
            self.Y_max = -(-np.amax(np.amax(ranged_data))//1000)*1000

        types = list(set(itertools.chain.from_iterable(row for row in self.positions.values)))
        types_dict = dict(zip(types, [[] for _ in range(len(types))]))

        for key in self.plot_data.columns:
            types_dict[col_posi_linker(key)].append(self.plot_data[key])
        del types_dict[0]
        self.types_dict = types_dict

        print("Welcome to chlamy bioluminescence visualizer!")

    """
    def col_posi_linker(col_name):
        if col_name[1] == "0":
            return self.positions.at[col_name[0], col_name[2]]
        else :
            return self.positions.at[col_name[0], col_name[1:3]]
    """

    def overview(self, graph_width = 4, graph_length = 4, col_number = 3):
        data_types_dict = self.types_dict
        # return self.plot_data
        # print(data_types_dict)
        plot_count : int = 1
        fig = plt.figure(figsize=(col_number*graph_width, -(-len(data_types_dict)//col_number)*graph_length))
        fig.suptitle('Overview')
        for key, value in data_types_dict.items():
            ax =  fig.add_subplot(len(data_types_dict)//col_number+1, col_number, plot_count)
            for col in value:
                ax.plot(col.index, col, color=self.subtitle_and_color[key][0])
            plot_count : int = plot_count + 1

            n_rythm : int = int(-(-((len(value[0])-1)//(60/self.common_setting["sampling_period"]))//24))

            ax.set_title(f'{self.subtitle_and_color[key][1]} (No.{key}), {len(value)}well')
            ax.set_xticks(np.linspace(0, int(n_rythm*24), n_rythm+1))
            ax.set_xticks(np.linspace(0, int(n_rythm*24), n_rythm*4+1), minor=True)
            ax.set_xlabel(self.common_setting["x_axis_title"])
            if self.common_setting["yaxis_share_switch"]:
                ax.set_ylim(0, self.Y_max)
            ax.set_ylabel(self.common_setting["y_axis_title"])
            ax.grid(axis="both")

        fig.tight_layout()
        if self.common_setting["plot_save_switch"]: # == 1
            plt.savefig(self.common_setting["save_path"] + f"overview_{col_number}_col_plot.jpg")
        else :
            pass
        plt.show()


    # MTとWTとかの系統単位での比較
    def strain_compare(self, strain_compare_info={}, graph_width = 4, graph_length = 4, col_number = 2):
        if len(strain_compare_info) < 1:
            print("No comparison.")
            return
        else :
            data_types_dict = self.types_dict
            plot_count : int = 1
            fig = plt.figure(figsize=(col_number*graph_width, -(-len(strain_compare_info)//col_number)*graph_length))
            fig.suptitle('Strains comparison')
            for graph_name, value in strain_compare_info.items():
                handles = []
                labels = []
                ax =  fig.add_subplot(-(-len(strain_compare_info)//col_number), col_number, plot_count)
                for type_number in value:
                    try :
                        for col in data_types_dict[type_number]:
                            line = ax.plot(col.index, col, color=self.subtitle_and_color[type_number][0])
                    except KeyError:
                        print(f"エラー：系統番号 {type_number} は96well_positionsに登録されていません。")
                        return
                    else :
                        handles.append(line[0])
                        labels.append(self.subtitle_and_color[type_number][1])
                ax.legend(handles, labels)
                plot_count = plot_count + 1

                n_rythm = int(-(-((len(data_types_dict[type_number][0])-1)/(60/self.common_setting["sampling_period"]))//24))
                ax.set_title(graph_name)
                ax.set_xticks(np.linspace(0, int(n_rythm*24), n_rythm+1))
                ax.set_xticks(np.linspace(0, int(n_rythm*24), n_rythm*4+1), minor=True)
                ax.set_xlabel(self.common_setting["x_axis_title"])
                if self.common_setting["yaxis_share_switch"]:
                    ax.set_ylim(0, self.Y_max)
                ax.set_ylabel(self.common_setting["y_axis_title"])
                ax.grid(axis="both")

            fig.tight_layout()
            if self.common_setting["plot_save_switch"]: # == 1
                plt.savefig(self.common_setting["save_path"] + f"compare_plot.jpg")
            else :
                pass
            plt.show()


    # 株単位での比較
    def clone_compare(self, clone_compare_info={}, random_color = 0, graph_width = 4, graph_length = 4, col_number = 2):
        if len(clone_compare_info) < 1:
            print("No clone comparison.")
        else :
            def col_posi_linker(col_name, positions):
                if col_name[1] == "0":
                    return positions.at[col_name[0], col_name[2]]
                else :
                    return positions.at[col_name[0], col_name[1:3]]

            fig = plt.figure(figsize=(col_number*graph_width, -(-len(clone_compare_info)//col_number)*graph_length))
            fig.suptitle('Clones comparison')
            plot_count = 1
            for title, clones_tuple in clone_compare_info.items():
                ax =  fig.add_subplot(-(-len(clone_compare_info)//col_number), col_number, plot_count)
                if random_color :
                    try :
                        for col_name in clones_tuple:
                            subtitle_and_color_ = self.subtitle_and_color[col_posi_linker(col_name, self.positions)]
                            ax.plot(self.plot_data[col_name].index, self.plot_data[col_name], label=col_name+f' ({subtitle_and_color_[1]})')
                    except KeyError:
                        print(f"Error : No such cell -> {col_name}")
                        return 
                else :
                    try :
                        for col_name in clones_tuple:
                            subtitle_and_color_ = self.subtitle_and_color[col_posi_linker(col_name, self.positions)]
                            ax.plot(self.plot_data[col_name].index, self.plot_data[col_name], color=subtitle_and_color_[0], label=col_name+f' ({subtitle_and_color_[1]})')
                    except KeyError:
                        print(f"Error : No such cell -> {col_name}")
                        return 
                ax.legend()
                plot_count = plot_count + 1

                n_rythm = int(-(-((len(self.plot_data)-1)/(60/self.common_setting["sampling_period"]))//24))
                ax.set_title(title)
                ax.set_xticks(np.linspace(0, int(n_rythm*24), n_rythm+1))
                ax.set_xticks(np.linspace(0, int(n_rythm*24), n_rythm*4+1), minor=True)
                ax.set_xlabel(self.common_setting["x_axis_title"])
                if self.common_setting["yaxis_share_switch"]:
                    ax.set_ylim(0, self.Y_max)
                ax.set_ylabel(self.common_setting["y_axis_title"])
                ax.grid(axis="both")

            fig.tight_layout()
            if self.common_setting["plot_save_switch"]: # == 1
                plt.savefig(self.common_setting["save_path"] + f"clone_compare_plot.jpg")
            else :
                pass
            plt.show()


    def all(self, graph_width = 2.5, graph_length = 2.5, col_number = 12, blank_off = 1):
        def col_posi_linker(col_name, positions):
            if col_name[1] == "0":
                return positions.at[col_name[0], col_name[2]]
            else :
                return positions.at[col_name[0], col_name[1:3]]

        fig = plt.figure(figsize=(col_number*graph_width, -(-len(self.plot_data.columns)//col_number)*graph_length))
        fig.suptitle('All')
        plot_count = 1
        for col in self.plot_data:
            ax =  fig.add_subplot(-(-len(self.plot_data.columns)//col_number), col_number, plot_count)
            if col_posi_linker(col, self.positions):
                ax.plot(self.plot_data.index, self.plot_data[col], color = self.subtitle_and_color[col_posi_linker(col, self.positions)][0])
            else : # col_posi_linker(col, positions) == 0
                if blank_off:
                    ax.plot(self.plot_data.index, [0]*len(self.plot_data.index), color = "black")
                else :
                    ax.plot(self.plot_data.index, self.plot_data[col], color = "black")
            plot_count = plot_count + 1

            n_rythm = int(-(-((len(self.plot_data[col])-1)/(60/self.common_setting["sampling_period"]))//24))
            ax.set_title(col)
            ax.set_xticks(np.linspace(0, int(n_rythm*24), n_rythm+1))
            ax.set_xticks(np.linspace(0, int(n_rythm*24), n_rythm*4+1), minor=True)
            ax.set_xlabel(self.common_setting["x_axis_title"])
            if self.common_setting["yaxis_share_switch"]:
                ax.set_ylim(0, self.Y_max)
            ax.set_ylabel(self.common_setting["y_axis_title"])
            ax.grid(axis="both")

        fig.tight_layout()
        if self.common_setting["plot_save_switch"]: # == 1
            plt.savefig(self.common_setting["save_path"] + f"all_plot.jpg")
        else :
            pass
        plt.show()

