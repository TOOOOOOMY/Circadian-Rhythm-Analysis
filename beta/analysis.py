
import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
%matplotlib inline


settings = {
    "x_axis_title" : "Time [h]",
    "y_axis_title" : "Bioluminescence",
    "column_number" : 5,
    "overwrite_column_number" : 4,
    "y_axis_share_switch" : 1,
    "yaxis_percentage_switch" : 1,
    "over_view_image_length" : 4.5,
    "over_view_image_width" : 5.0,
    "all_plot_column_number" : 12,
    "all_plot_image_length" : 2.5,
    "all_plot_image_width" : 2.5
}


settings_2 = {
    0 : ["black", "Non"],
    1 : ["red", "TOC1-Resi-R"],
    2 : ["orange", "TOC1-Resi-AR"],
    3 : ["green", "TOC1-Sens-R"],
    4 : ["lightgreen", "TOC1-Sens-AR"],
    5 : ["blue", "CBR"],
    6 : ["lightblue", "Group6"],
    7 : ["orangered", "PRR1-Resi-R"],
    8 : ["salmon", "PRR1-Resi-AR"],
    9 : ["forestgreen", "PRR1-Sens-R"],
    10 : ["limegreen", "PRR1-Sens-AR"],
}


def visualizer(file_name, # include .csv -> sample.csv
               file_path = "", # /content/sample.csv -> /content/
               graph_settings = settings,
               subtitle_and_color = settings_2,
               overlap_dict = {},
               file_from = 1,
               sampling_period = 60,
               estimated_period = 24,
               over_view_plot_switch = 1,
                all_plot_switch = 1
    ):

    ##x軸単位（「"」に囲まれた部分を書き換え、以下同じ）
    x_axis_title = graph_settings["x_axis_title"]
    ##y軸単位
    y_axis_title = graph_settings["y_axis_title"]

    ##Overview plotでのグラフ横列表示数（１～５、標準３）
    column_number = graph_settings["column_number"]

    ##All plotでのグラフ間Y軸共有の有無（共有無→０、有→１）
    y_axis_share_switch = graph_settings["y_axis_share_switch"]

    ##６-２：Y軸を各データの最大値に対する%とする場合は１
    yaxis_percentage_switch = graph_settings["yaxis_percentage_switch"]

    ##グループ番号毎の色（参考：https://matplotlib.org/examples/color/named_colors.html）、先頭から数字の０に対応

    ##Overview plot
    ###画像1枚あたりの縦サイズ
    ov_length = graph_settings["over_view_image_length"]
    ###画像1枚あたりの横サイズ
    ov_width = graph_settings["over_view_image_width"]

    ##
    overwrite_column_number = graph_settings["overwrite_column_number"]

    ##All plot
    ###出力時の列数
    a_column = graph_settings["all_plot_column_number"]
    ###画像1枚あたりの縦サイズ
    a_length = graph_settings["all_plot_image_length"]
    ###画像1枚あたりの横サイズ
    a_width = graph_settings["all_plot_image_width"]

    #Import data
    row_data = pd.read_csv(file_name+".csv", engine="python", encoding="utf-8_sig")

    try:
        new_data = row_data.drop('Unnamed: 0', axis=1).T
        X_axis = round(row_data["Unnamed: 0"].iloc[1:].reset_index(drop=True).astype(float), 4)
    except KeyError:
        new_data = row_data.drop('Time', axis=1).T
        X_axis = round(row_data['Time'].iloc[1:].reset_index(drop=True).astype(float), 4)


    #全体データとして耐性欄を削除
    data_ALL = new_data.drop(0, axis=1)

    #P耐性を抽出.同欄を削除
    data_P_Resi = new_data[new_data[0]==1].drop(0, axis=1)

    #P感受性を抽出.同欄を削除
    data_Non_Resi = new_data[new_data[0]==0].drop(0, axis=1)

    #最大値取得→グラフのY軸共通化に使用
    F_max = np.amax(np.amax(new_data))
    Y_max = round(F_max, -1*(len(str(F_max)) - 3)) #(最大-1)桁で切り上げ、-3は仕様（不思議に思った場合はlen(str(F_max))とF_maxを出力してみること）

    color_list = ["black", "red", "orange", "green", "lightgreen", "blue", "lightblue", "yellow", "teal", "cyan",  "gray"]
    ##Reference:https://matplotlib.org/examples/color/named_colors.html

    subtitle_list = ["G0", "Resi", "G2", "Sens", "G4", "CBR", "G6", "G7", "G8", "G9", "G10"]

    savefig_path = ""


    ##########
    #スイッチ
    peak_overwrite_switch = 1 # 0:off, 1:on

    #Filter
    ##最短周期[h]
    start_point = 12
    ##最長周期[h]
    end_point = 48

    #detector
    peak_dtector_starts_point = 12 #3以上
    ##########

    def file_saver(def_name, choice, file_name, savefig_path):
        image_name = file_name + " - " + def_name + " plot (" + choice + ")"
        filename = savefig_path + "{}.jpg".format(image_name)
        plt.savefig(filename) #plt.show()より前に書くこと

    def File_saver(name, file_name, savefig_path):
        image_name = file_name + " - " + name + " plot"
        filename = savefig_path + "{}.jpg".format(image_name)
        plt.savefig(filename) #plt.show()より前に書くこと


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


    def color_changer(data_number):
        COLOR = subtitle_and_color[int(data_number)][0] # color_list[int(data_number)]
        Subtitle = subtitle_and_color[int(data_number)][1] # subtitle_list[int(data_number)]
        return COLOR, Subtitle


    def rfft_plot(ax, xaxis, data, clr):
            ax.plot(xaxis, data, color='{}'.format(clr), zorder=1)
            plt.xlabel("time [h]")
            plt.ylabel("fluorescence")


    def fft_plot(ax, xaxis, data, clr):
            ax.plot(xaxis, data, color='{}'.format(clr))
            plt.xlabel("frequency")
            plt.ylabel("amplitude")


    def range_1_local_max_detector (ax, xaxis, yaxis):
        #ピーク量
        Peek_size = []

        #ピーク位置時間
        Peek_time = []

        for i in range(peak_dtector_starts_point, len(xaxis)-1):
            dif1 = int(yaxis[i] - yaxis[i-1]) 
            dif2 = int(yaxis[i+1] - yaxis[i])
            if dif1 > 0 and dif2 < 0 :
                Peek_size.append(yaxis[i])
                Peek_time.append(xaxis[i])
            elif dif1 > 0 and dif2 == 0 :
                Peek_size.append(yaxis[i])
                Peek_time.append(xaxis[i]+(xaxis[i+1]-xaxis[i])/2)
                print("Middle -> {0}".format(i))
        if peak_overwrite_switch ==1:        
            ax.scatter(Peek_time, Peek_size, color="gold", zorder=2, marker="o", label='peak_local_maximum')
        
        return len(Peek_size)


    def range_2_local_max_detector (ax, xaxis, yaxis):
        #ピーク量
        Peek_size = []

        #ピーク位置時間
        Peek_time = []

        for i in range(peak_dtector_starts_point, len(xaxis)-2):
            slope2 = int(yaxis[i-1] - yaxis[i-2])
            slope3 = int(yaxis[i] - yaxis[i-1]) 
            slope4 = int(yaxis[i+1] - yaxis[i])
            slope5 = int(yaxis[i+2] - yaxis[i+1]) 
            if (slope2 >= 0 and
                slope5 <= 0):
                if slope3 > 0 and slope4 < 0 :
                    Peek_size.append(yaxis[i])
                    Peek_time.append(xaxis[i])
                elif slope3 == 0 and slope4 == 0 :
                    Peek_size.append(yaxis[i])
                    Peek_time.append(xaxis[i]+(xaxis[i+1]-xaxis[i])/2)
                    print("Middle -> {0}".format(i))
        
        if peak_overwrite_switch ==1: 
            ax.scatter(Peek_time, Peek_size, color="gold", zorder=2, marker="o", label='peak_local_maximum')
        
        return len(Peek_size)


    def new_local_max_detector (ax, xaxis, yaxis):
        #ピーク量
        Peek_size = []

        #ピーク位置時間
        Peek_time = []

        for i in range(peak_dtector_starts_point, len(xaxis)-4):
            cmp_list = [yaxis[i+4], yaxis[i+3], yaxis[i+2], yaxis[i+1], yaxis[i], yaxis[i-1], yaxis[i-2], yaxis[i-3]]
            if max(cmp_list) == yaxis[i]:
                if cmp_list.count(yaxis[i]) == 1:
                    Peek_size.append(yaxis[i])
                    Peek_time.append(xaxis[i])
                elif cmp_list.count(yaxis[i]) == 2:
                    if yaxis[i] == yaxis[i+1]:
                        Peek_size.append(yaxis[i])
                        Peek_time.append(xaxis[i]+(xaxis[i+1]-xaxis[i])/2)
                    elif yaxis[i] == yaxis[i+2]:                 
                        Peek_size.append(yaxis[i+1])
                        Peek_time.append(xaxis[i+1])
                    elif yaxis[i] == yaxis[i+3]: 
                        Peek_size.append(yaxis[i])
                        Peek_time.append(xaxis[i+1]+(xaxis[i+2]-xaxis[i+1])/2)
                    else :
                        print("Error : Unexpected 2 maxs pattern.")
                        print(cmp_list)
                elif cmp_list.count(yaxis[i]) == 3:
                    if yaxis[i] == yaxis[i+1] == yaxis[i+2]:
                        Peek_size.append(yaxis[i+1])
                        Peek_time.append(xaxis[i+1])
                    elif yaxis[i] == yaxis[i+1] == yaxis[i+3] or yaxis[i] == yaxis[i+2] == yaxis[i+3]:
                        Peek_size.append(yaxis[i])
                        Peek_time.append(xaxis[i+1]+(xaxis[i+2]-xaxis[i+1])/2)
                    elif yaxis[i] == yaxis[i+2] == yaxis[i+4]:
                        Peek_size.append(yaxis[i+2])
                        Peek_time.append(xaxis[i+2])
                    else :
                        print("Error : Unexpected 3 maxs pattern.")
                elif cmp_list.count(yaxis[i]) == 4:
                    print("Error : Unexpected 4 maxs pattern.")
                else :
                    print("Error : Unexpected maxs pattern.")
            else :
                pass
        if peak_overwrite_switch ==1: 
            ax.scatter(Peek_time, Peek_size, color="gold", zorder=2, marker="o", label='peak_local_maximum')
        
        return len(Peek_size)


    def range_3_local_max_detector (ax, xaxis, yaxis):
        #ピーク量
        Peek_size = []

        #ピーク位置時間
        Peek_time = []

        for i in range(peak_dtector_starts_point, len(xaxis)-3):
            slope1 = int(yaxis[i-2] - yaxis[i-3]) 
            slope2 = int(yaxis[i-1] - yaxis[i-2])
            slope3 = int(yaxis[i] - yaxis[i-1]) 
            slope4 = int(yaxis[i+1] - yaxis[i])
            slope5 = int(yaxis[i+2] - yaxis[i+1]) 
            slope6 = int(yaxis[i+3] - yaxis[i+2])
            if (slope1 > 0 and
                slope2 >= 0 and
                slope5 <= 0 and
                slope6 < 0):
                if slope3 > 0 and slope4 < 0 :
                    Peek_size.append(yaxis[i])
                    Peek_time.append(xaxis[i])
                elif slope3 == 0 and slope4 == 0 :
                    Peek_size.append(yaxis[i])
                    Peek_time.append(xaxis[i]+(xaxis[i+1]-xaxis[i])/2)
                    print("Middle -> {0}".format(i))
        
        if peak_overwrite_switch ==1: 
            ax.scatter(Peek_time, Peek_size, color="gold", zorder=2, marker="o", label='peak_local_maximum')
        
        return len(Peek_size)


    def plot_choice(X_axis, new_data, file_name, savefig_path, Yaxis):
        F_max = np.amax(np.amax(new_data))
        Y_max = -(-F_max//1000)*1000

        for I in range(2, 7):
            fig = plt.figure(figsize=(a_column*a_width, -(-new_data.shape[0]//a_column)*a_length))
            for i in range(1, new_data.shape[0]+1):
                ax =  fig.add_subplot(-(-new_data.shape[0]//a_column),a_column,i)

                ROW, Col = well_namer(i)

                Name = '{0}{1}'.format(ROW, Col)
                show = new_data.T[Name]

                COLOR, Subtitle = color_changer(show[0])
                target_col_data = show.drop(0, axis=0).reset_index(drop=True).values
                if yaxis_percentage_switch == 1:
                    Shaped_data = target_col_data/max(target_col_data)*100
                else :
                    Shaped_data = target_col_data
                ymax = np.amax(Shaped_data)
                data_time_lenght = len(Shaped_data)
                n_rythm = -(-data_time_lenght//24) #データに含まれる24時間周期数
                X_max = n_rythm*24 #X軸長さ

                if show[0] == 0:
                    ax.plot(0, 0, color=COLOR, zorder=1)
                else :
                    if I == 2:
                        header = "Original plot"
                        period_plot_switch = 0
                        rfft_plot(ax, X_axis, Shaped_data, COLOR)
                        
                    elif I == 1 :
                        print("Skip : I = 2")
                        
                    elif I == 3 :
                        header = "r1_detector plot"
                        No_of_peak = " ({} ps)".format(range_1_local_max_detector(ax, X_axis, Shaped_data))
                        rfft_plot(ax, X_axis, Shaped_data, COLOR)

                    elif I == 4 :
                        header = "r2_detector plot"
                        No_of_peak = " ({} ps)".format(range_2_local_max_detector(ax, X_axis, Shaped_data))
                        rfft_plot(ax, X_axis, Shaped_data, COLOR)

                    elif I == 5 :
                        header = "r3_detector plot"
                        No_of_peak = " ({} ps)".format(range_3_local_max_detector(ax, X_axis, Shaped_data))
                        rfft_plot(ax, X_axis, Shaped_data, COLOR)

                    elif I == 6 :
                        header = "new_local_max_detector plot"
                        No_of_peak = " ({} ps)".format(new_local_max_detector(ax, X_axis, Shaped_data))
                        rfft_plot(ax, X_axis, Shaped_data, COLOR)

                    else :
                        print("Skip")


                ax.set_title('{0}{1} ({2})'.format(ROW, Col, Subtitle))
                ax.set_xticks(np.linspace(0, X_max, n_rythm+1)) # x 軸 (major) 目盛り設定
                ax.set_xticks(np.linspace(0, X_max, n_rythm*4+1), minor=True) # x 軸 (minor) 目盛り設定
                ax.grid(axis="both") #xy両方のグリットを表示

            Title = file_name + ' - ' + header
            fig.tight_layout()
            fig.suptitle(Title, fontsize=25)
            plt.subplots_adjust(top=0.95, left=0.05, bottom=0.08)
            fig.text(0.5, 0.02, 'frequency', ha='center', va='center', fontsize=15)
            fig.text(0.02, 0.5, 'amplitude', ha='center', va='center', rotation='vertical', fontsize=15)
            fig.align_labels()
            image_name = file_name
            plt.savefig( "{}.jpg".format(Title))
            #file_saver("96well(%)", "-", data_name, savefig_path)
            plt.show()

    """
    実行関数
    """
    plot_choice(X_axis, new_data, file_name, savefig_path, Yaxis)
    


"""
実行方法
"""
visualizer("200629", # include .csv -> sample.csv
               file_path = "", # /content/sample.csv -> /content/
               graph_settings = settings,
               subtitle_and_color = settings_2,
               overlap_dict = {},
               file_from = 1,
               sampling_period = 60,
               estimated_period = 24,
               over_view_plot_switch = 1,
                all_plot_switch = 1
)
    
