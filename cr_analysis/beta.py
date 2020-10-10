"""
==========
Author: Tomoki WATANABE
Update: 01/07/2020
Version: 3.0.0
License: BSD License
Programing Language: Python3
==========
"""

# 20200710
# 移動平均実装

import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# graph_settings
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


setting_3 = {}

# analysis switch
setting_4 = {
    "Original plot" : 0,
    "r1_detector plot" : 0,
    "r2_detector plot" : 0,
    "r3_detector plot" : 0,
    "new_local_max_detector plot" : 0,
    "period plot" : 0,
    "moving_average plot" : 1
}

# analysis setings
setting_5 = {
    # detector
    "peak_dtector_starts_point" : 6 #3以上
}


def visualizer(file_name, # include .csv -> sample.csv
               file_path = "", # /content/sample.csv -> /content/
               graph_settings = settings,
               subtitle_and_color = settings_2,
               overlap_dict = setting_3,
               analysis_plot_dict = setting_4,
               analysis_settings = setting_5,
               file_from = 1, #Lumicecの場合は0
               sampling_period = 60,
               estimated_period = 24,
               over_view_plot_switch = 1,
                all_plot_switch = 0
    ):

    x_axis_title = graph_settings["x_axis_title"]

    y_axis_title = graph_settings["y_axis_title"]

    ##Overview以外のplotでのグラフ横列表示数（１～５、標準３）
    column_number = graph_settings["column_number"]

    ##Overview plotでのグラフ横列表示数（１～５、標準３）
    overwrite_column_number = graph_settings["overwrite_column_number"]

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

    ##All plot
    ###出力時の列数
    a_column = graph_settings["all_plot_column_number"]
    ###画像1枚あたりの縦サイズ
    a_length = graph_settings["all_plot_image_length"]
    ###画像1枚あたりの横サイズ
    a_width = graph_settings["all_plot_image_width"]

    """
    Support functions
    """
    def color_changer(data_number):
        COLOR = subtitle_and_color[int(data_number)][0] # color_list[int(data_number)]
        Subtitle = subtitle_and_color[int(data_number)][1] # subtitle_list[int(data_number)]
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


    def percentage_data_transfer(shaped_data):
        cnt_list = []
        for col in shaped_data.T.columns:
            # print(col)
            target_data = shaped_data.drop(0, axis=1).T[col]
            cnt_list.append([shaped_data.T[col][0]]+list(target_data/max(target_data)*100))
        return pd.DataFrame(cnt_list, columns=shaped_data.T.index, index=shaped_data.T.columns)


    """
    main functions
    """
    def colored_overview_n_columns(X_axis, shaped_data, data_name, Yaxis, n, x_axis_title, y_axis_title):
        group_list = sorted(list(set(shaped_data[0])))

        if yaxis_percentage_switch == 1:
            new_data = percentage_data_transfer(shaped_data)
            Y_max = 100
        else :
            new_data = shaped_data
            F_max = np.amax(np.amax(new_data.drop(0, axis=1)))
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
                process_data = new_data.drop(0, axis=1).T.reset_index(drop=True)
                name = 'ALL'
                color_number = "-"
                plot_line_list = []
                for i in range(0, len(group_list)):
                    plot_line = ax.plot(X_axis, new_data[new_data[0]==group_list[i]].drop(0, axis=1).T.reset_index(drop=True), color='{}'.format(subtitle_and_color[round(group_list[i])][0]), label=subtitle_and_color[round(group_list[i])][1])
                    # plot_line = ax.plot(X_axis, new_data[new_data[0]==group_list[i]].drop(0, axis=1).T.reset_index(drop=True), color='{}'.format(subtitle_and_color[round(group_list[i])][0]), label=subtitle_and_color[round(group_list[i])][1])
                    plot_line_list.append(plot_line[0])
                ax.legend(plot_line_list, plot_line_list)
            else :
                process_data = new_data[new_data[0]==group_list[I-1]].drop(0, axis=1).T.reset_index(drop=True)
                name = subtitle_and_color[round(group_list[I-1])][1]
                color_number = "No.{}".format(round(group_list[I-1]))
                ax.plot(X_axis, process_data, color='{}'.format(subtitle_and_color[round(group_list[I-1])][0])) # color_list[round(group_list[I-1])]))
            #変数セット
            data_time_lenght = len(process_data)
            n_rythm = int(-(-(data_time_lenght/(60/sampling_period))//24))
            X_max = int(n_rythm*24)
            original_lenght = len(new_data.drop(0, axis=1))
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


    def overlap_write(overlap_dict, X_axis, shaped_data, data_name, Yaxis, column_number, x_axis_title, y_axis_title):
        group_list = sorted(list(set(shaped_data[0])))
        if yaxis_percentage_switch == 1:
            new_data = percentage_data_transfer(shaped_data)
            Y_max = 100
        else :
            new_data = shaped_data
            F_max = np.amax(np.amax(new_data.drop(0, axis=1)))
            Y_max = -(-F_max//1000)*1000
        fig = plt.figure(figsize=(column_number*ov_width, -(-(len(overlap_dict)+column_number)//column_number)*ov_length))
        # for I in range (0, len(group_list)+1, 1):
        count = 0
        print("column_number = {0}".format(column_number))
        for title in overlap_dict.keys():
            ax =  fig.add_subplot(-(-(len(overlap_dict)+column_number)//column_number), column_number, count+1)
            plot_line_list = []
            for i in overlap_dict[title]:
                plot_line = ax.plot(X_axis, new_data[new_data[0]==i].drop(0, axis=1).T.reset_index(drop=True), color='{}'.format(subtitle_and_color[i][0]), label=subtitle_and_color[i][1])
                plot_line_list.append(plot_line[0])
            ax.legend(plot_line_list, plot_line_list)
            #変数セット
            data_time_lenght = len(new_data.drop(0, axis=1).T)
            n_rythm = int(-(-(data_time_lenght/(60/sampling_period))//24))
            X_max = int(n_rythm*24)
            each_title = '{0}'.format(title)
            ax.set_title(each_title)
            ax.set_xticks(np.linspace(0, X_max, n_rythm+1))
            ax.set_xticks(np.linspace(0, X_max, n_rythm*4+1), minor=True)
            ax.set_xlabel(x_axis_title)
            if Yaxis == "Y shared":
                ax.set_ylim(0, Y_max)
            ax.set_ylabel(y_axis_title)
            ax.grid(axis="both")
            count = count + 1
        fig.tight_layout()
        plt.savefig( "overlap_col_plot.jpg")
        plt.show()
        return 


    def all_plot(X_axis, shaped_data, data_name, Yaxis):
        if yaxis_percentage_switch == 1:
            new_data = percentage_data_transfer(shaped_data)
            Y_max = 100
        else :
            new_data = shaped_data
            F_max = np.amax(np.amax(new_data.drop(0, axis=1)))
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

            #変数セット
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


    def analysis_plot(X_axis, new_data, file_name, Yaxis, analysis_plot_dict, analysis_settings):
  
        def rfft_plot(ax, xaxis, data, clr):
                ax.plot(xaxis, data, color='{}'.format(clr), zorder=1)
                plt.xlabel("time [h]")
                plt.ylabel("fluorescence")

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
                    # print("Middle -> {0}".format(i))
            # if peak_overwrite_switch ==1:        
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
                        # print("Middle -> {0}".format(i))
            
            # if peak_overwrite_switch ==1: 
            ax.scatter(Peek_time, Peek_size, color="gold", zorder=2, marker="o", label='peak_local_maximum')
            
            return len(Peek_size)

        def new_local_max_detector (ax, xaxis, yaxis, peak_overwrite_switch =1):
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
                        # 重複
                        elif yaxis[i] == yaxis[i-1] or yaxis[i] == yaxis[i-2] or yaxis[i] == yaxis[i-3]:
                            pass
                        else :
                            print("Error : Unexpected 2 maxs pattern.")
                            print(cmp_list)
                    elif cmp_list.count(yaxis[i]) == 3:
                        if yaxis[i] == yaxis[i+1] == yaxis[i+2]:
                            Peek_size.append(yaxis[i+1])
                            Peek_time.append(xaxis[i+1])
                        # 重複
                        elif yaxis[i-1] == yaxis[i] == yaxis[i+1] or yaxis[i] == yaxis[i-1] == yaxis[i-2]:
                            pass
                        elif yaxis[i] == yaxis[i+1] == yaxis[i+3] or yaxis[i] == yaxis[i+2] == yaxis[i+3]:
                            Peek_size.append(yaxis[i])
                            Peek_time.append(xaxis[i+1]+(xaxis[i+2]-xaxis[i+1])/2)
                        # 重複
                        elif yaxis[i-1] == yaxis[i] == yaxis[i+2] or yaxis[i-3] == yaxis[i-1] == yaxis[i] or yaxis[i-2] == yaxis[i] == yaxis[i+1] or yaxis[i-3] == yaxis[i-2] == yaxis[i]:
                            pass
                        elif yaxis[i] == yaxis[i+2] == yaxis[i+4]:
                            Peek_size.append(yaxis[i+2])
                            Peek_time.append(xaxis[i+2])
                        # 重複
                        elif yaxis[i-2] == yaxis[i] == yaxis[i+2] or yaxis[i-4] == yaxis[i-2] == yaxis[i]:
                            pass
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
            
            return Peek_time

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
                        # print("Middle -> {0}".format(i))
            
            # if peak_overwrite_switch ==1: 
            ax.scatter(Peek_time, Peek_size, color="gold", zorder=2, marker="o", label='peak_local_maximum')
            
            return len(Peek_size)

        def period_plot(y_max):
            def period_plot_(ax, xaxis, yaxis, COLOR, min_period, min_period_num, max_period):
                period_list = []
                peak_time = new_local_max_detector (ax, xaxis, yaxis, peak_overwrite_switch =0)
                for i in range(1, len(peak_time), 1):
                    dif = peak_time[i] - peak_time[i-1]
                    if dif >= min_period and dif <= max_period:
                        period_list.append(dif)
                    else :
                        break
                if len(period_list) >= min_period_num:
                    ax.bar([i for i in range(1, len(period_list)+1, 1)], period_list, color=COLOR)
                else :
                    ax.bar(0, 0, color=COLOR)
                return 

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
                # ymax = np.amax(Shaped_data)
                data_time_lenght = len(Shaped_data)
                n_rythm = -(-data_time_lenght//24) #データに含まれる24時間周期数
                X_max = n_rythm*24 #X軸長さ

                if show[0] == 0:
                    ax.plot(0, 0, color=COLOR, zorder=1)
                else :
                    period_plot_(ax, X_axis, Shaped_data, COLOR, 12, 2, y_max)
                ax.set_title('{0}{1} ({2})'.format(ROW, Col, Subtitle))
                ax.set_xticks(np.linspace(1, 5, 5)) # # x 軸 (major) 目盛り設定
                # ax.set_xticks(np.linspace(0, 5), minor=True) # x 軸 (minor) 目盛り設定
                ax.set_yticks(np.linspace(0, y_max, int(y_max/4+1))) # # y 軸 (major) 目盛り設定
                ax.grid(axis="both") #xy両方のグリットを表示

            title = file_name.replace(".csv", "") + ' - ' + analysis_type
            fig.tight_layout()
            fig.suptitle(title, fontsize=25)
            plt.subplots_adjust(top=0.95, left=0.05, bottom=0.08)
            fig.text(0.5, 0.02, 'frequency', ha='center', va='center', fontsize=15)
            fig.text(0.02, 0.5, 'amplitude', ha='center', va='center', rotation='vertical', fontsize=15)
            fig.align_labels()
            image_name = file_name
            plt.savefig( "{}.jpg".format(title))
            plt.show()

        def moving_avrg(xaxis, yaxis, assumed_period = 24):
            if isinstance(assumed_period, int):
                assumed_half_period = round((assumed_period - 1)/2)
                cal_range = len(xaxis) - assumed_period
                new_xaxis = xaxis[assumed_half_period:-assumed_half_period]
                new_yaxis = []
                if len(new_xaxis) < 1:
                    print("Error : Cannot calculate with this range.")
                    return
                elif assumed_period % 2 == 0: # 偶数
                    for i in range(1, cal_range+1, 1):
                        new_yaxis.append(statistics.mean(yaxis[i:i+assumed_period-1])+(yaxis[i-1] + yaxis[i+assumed_period-1])/2)
                else :
                    for i in range(1, cal_range+1, 1):
                        new_yaxis.append(statistics.mean(yaxis[i-1:i+assumed_period]))
                l_max = max(new_yaxis)
                return [0]*assumed_half_period + list(map(lambda x: x/l_max, new_yaxis)) + [0]*assumed_half_period
            else :
                print("assumed_period should be integer.")

        F_max = np.amax(np.amax(new_data))
        Y_max = -(-F_max//1000)*1000

        ## Analysis
        peak_dtector_starts_point = analysis_settings["peak_dtector_starts_point"]

        for analysis_type, switch in analysis_plot_dict.items():
            if switch != 1:
                continue
            elif  analysis_type == "period plot":
                period_plot(32)
            else :
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
                        if analysis_type == "Original plot":
                            pass
                        elif analysis_type == "r1_detector plot":
                            No_of_peak = " ({} ps)".format(range_1_local_max_detector(ax, X_axis, Shaped_data))
                        elif analysis_type == "r2_detector plot":
                            No_of_peak = " ({} ps)".format(range_2_local_max_detector(ax, X_axis, Shaped_data))
                        elif analysis_type == "r3_detector plot":
                            No_of_peak = " ({} ps)".format(range_3_local_max_detector(ax, X_axis, Shaped_data))
                        elif analysis_type == "new_local_max_detector plot":
                            _ = new_local_max_detector(ax, X_axis, Shaped_data)
                            rfft_plot(ax, X_axis, Shaped_data, COLOR)
                        elif analysis_type == "moving_average plot":
                            ax.plot(X_axis, moving_avrg(X_axis, target_col_data), color=COLOR)
                        else :
                            print("Error : NOT defined function '{0}'.".format(analysis_type))
                        # rfft_plot(ax, X_axis, Shaped_data, COLOR)
                    ax.set_title('{0}{1} ({2})'.format(ROW, Col, Subtitle))
                    ax.set_xticks(np.linspace(0, X_max, n_rythm+1)) # x 軸 (major) 目盛り設定
                    ax.set_xticks(np.linspace(0, X_max, n_rythm*4+1), minor=True) # x 軸 (minor) 目盛り設定
                    ax.grid(axis="both") #xy両方のグリットを表示

                title = file_name.replace(".csv", "") + ' - ' + analysis_type
                fig.tight_layout()
                fig.suptitle(title, fontsize=25)
                plt.subplots_adjust(top=0.95, left=0.05, bottom=0.08)
                fig.text(0.5, 0.02, 'frequency', ha='center', va='center', fontsize=15)
                fig.text(0.02, 0.5, 'amplitude', ha='center', va='center', rotation='vertical', fontsize=15)
                fig.align_labels()
                image_name = file_name
                plt.savefig( "{}.jpg".format(title))
                plt.show()


    """
    処理分岐
    """

    def router(file_path, file_name, column_number, analysis_plot_dict, analysis_settings):
        if file_name[-4:] != ".csv":
            print("ERROR ->\nPlease use csv file.")
            sys.exit()
        row_data = pd.read_csv("{0}{1}".format(file_path, file_name), engine="python", encoding="utf-8_sig")
        try:
            shaped_data = row_data.drop('Unnamed: 0', axis=1).T
            X_axis = round(row_data["Unnamed: 0"].iloc[1:].reset_index(drop=True).astype(float), 4)
        except KeyError:
            shaped_data = row_data.drop('Time', axis=1).T
            X_axis = round(row_data['Time'].iloc[1:].reset_index(drop=True).astype(float), 4)
        finally:
            if y_axis_share_switch == 0:
                Yaxis = "Not shared"
            else :
                Yaxis = "Y shared"
            
            if over_view_plot_switch == 1:
                colored_overview_n_columns(X_axis, shaped_data, file_name, Yaxis, overwrite_column_number, x_axis_title, y_axis_title)
            else:
                pass

            if len(overlap_dict) > 0:
                overlap_write(overlap_dict, X_axis, shaped_data, file_name, Yaxis, column_number, x_axis_title, y_axis_title)
            else :
                pass

            if all_plot_switch == 1:
                all_plot(X_axis, shaped_data, file_name, Yaxis)
            else:
                pass
            
            analysis_plot(X_axis, shaped_data, file_name, Yaxis, analysis_plot_dict, analysis_settings)



    """
    実行関数
    """
    router(file_path, file_name, column_number, analysis_plot_dict, analysis_settings)
