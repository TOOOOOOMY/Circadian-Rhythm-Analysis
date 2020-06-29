#使い方
##０：左上にある「＞」をクリック

##１：「目次」「コードスニペット」「ファイル」のうち「ファイル」をクリック
##　（「ランタイム～」との表示が出ている場合は、自動で起動するまでしばらく(10秒ほど？)待つ　or　上のタブから「ランタイム」→「ランタイムを再起動」）

##２：「アップロード」から解析したいファイル（csv形式）をアップロード（「ランタイム～」の警告にはOKをクリック）

##３：下のfile_nameをアップロードしたファイル名（拡張子除く）に変更
file_name = "200629"  ##例：sample.csv→"sample"

##４：Y軸共有の有無を選択（共有無→０、有→１）
y_axis_share_switch = 1

##５-１：plotの有無を選択（無→０、有→１）
original_plot_switch = 1

original_fft_plot_switch = 1


##５-２：Overview plot表示時の列数を入力（１～５、標準３）
column_number = 3

##６：All plotの有無を選択（無→０、有→１）
all_plot_switch = 1

##７(Optional)：URLを参考に色を設定（https://matplotlib.org/examples/color/named_colors.html）、先頭から数字の０に対応
color_list = ["black", "red", "orange", "green", "lightgreen", "blue", "lightblue", "yellow", "teal", "cyan",  "gray"]

##８(Optional)：７で設定した色に対応するタイトルを設定
subtitle_list = ["G0", "Resi", "G2", "Sens", "G4", "G5", "G6", "G7", "G8", "G9", "G10"]

##９：Shiftキーを押しながらEnterキーを押す

##１０：「データ名＋グラフ名.jpg」の画像ファイルが左「ファイル」欄に生成されるまで待つ（待ち時間は通信状況等により変化します）

##１１：画像ファイルを右クリック→ダウンロード


#詳細設定
##Overview plot
###画像1枚あたりの縦サイズ
ov_length = 4.5  #標準4.5
###画像1枚あたりの横サイズ
ov_width = 5  #標準5.0

##All plot
###出力時の列数
a_column = 12  #標準12
###画像1枚あたりの縦サイズ
a_length = 2.5    #標準2.5
###画像1枚あたりの横サイズ
a_width = 2.5  #標準2.5


"""
==========
ここから下はいじらない
==========
"""
from scipy import signal
from statistics import stdev
%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.fftpack import fft

data_name = file_name
Imported_data = data_name+".csv"
n_contain = 8 #n-split, サブリストの要素数

#Import data
row_data = pd.read_csv(Imported_data, engine="python", encoding="utf-8_sig")

try:
    new_data = row_data.drop('Unnamed: 0', axis=1).T
    X_axis = round(row_data["Unnamed: 0"].iloc[1:].reset_index(drop=True).astype(float), 4)
except KeyError:
    new_data = row_data.drop('Time', axis=1).T
    X_axis = round(row_data['Time'].iloc[1:].reset_index(drop=True).astype(float), 4)


#説明列を削除、転置.最大蛍光値欄を削除
# new_data = row_data.drop('Unnamed: 0', axis=1).T.drop(1, axis=1)

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

savefig_path = "C:\\Users\\LEGO4\\IMAGE\\"


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

"""
def router(file_name, y_axis_switch, over_view_plot_switch, all_plot_switch, color_list, subtitle_list, column_number):
    row_data = pd.read_csv("{0}.csv".format(file_name), engine="python", encoding="utf-8_sig")
    new_data = row_data.drop('Unnamed: 0', axis=1).T.drop(1, axis=1)
    all_data = row_data.drop('Unnamed: 0', axis=1).T.drop(1, axis=1).drop(0, axis=1).T.reset_index(drop=True)
    X_axis = round(row_data["Unnamed: 0"].iloc[2:].reset_index(drop=True).astype(float), 4)
    data_name = file_name

    if y_axis_switch == 0:
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
"""

def file_saver(def_name, choice, data_name, savefig_path):
    image_name = data_name + " - " + def_name + " plot (" + choice + ")"
    filename = savefig_path + "{}.jpg".format(image_name)
    plt.savefig(filename) #plt.show()より前に書くこと

def File_saver(name, data_name, savefig_path):
    image_name = data_name + " - " + name + " plot"
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
    COLOR = color_list[int(data_number)]
    Subtitle = subtitle_list[int(data_number)]
    return COLOR, Subtitle


def rfft_plot(ax, xaxis, data, clr, name, subtitle, nop, x_max, n_rythm):
        ax.plot(xaxis, data, color='{}'.format(clr), zorder=1)
        plt.xlabel("time [h]")
        plt.ylabel("fluorescence")


def fft_plot(ax, xaxis, data, clr, name, subtitle, x_max, n_rythm):
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


def all_plot(X_axis, new_data, all_data, data_name, savefig_path, Yaxis):
    F_max = np.amax(np.amax(new_data))
    Y_max = -(-F_max//1000)*1000

    for I in range(1, 7):
        peak_time = []
        #fig = plt.figure(figsize=(30, 18))
        fig = plt.figure(figsize=(a_column*a_width, -(-new_data.shape[0]//a_column)*a_length))
        #for i in range(1, 97): #range(A, B) = AからB-1まで
        for i in range(1, new_data.shape[0]+1):
            ax =  fig.add_subplot(-(-new_data.shape[0]//a_column),a_column,i)

            ROW, Col = well_namer(i)

            Name = '{0}{1}'.format(ROW, Col)
            show = new_data.T[Name]

            COLOR, Subtitle = color_changer(show[0])

            Shaped_data = show.drop(0, axis=0).reset_index(drop=True).values
            ymax = np.amax(Shaped_data)
            data_time_lenght = len(Shaped_data)
            n_rythm = -(-data_time_lenght//24) #データに含まれる24時間周期数
            X_max = n_rythm*24 #X軸長さ

            filter_start = round(X_max/end_point)  #=5, end_point = 48h
            filter_end = round(X_max/start_point)  #=10, start_point = 12h

            if show[0] == 0:
                ax.plot(0, 0, color=COLOR, zorder=1)
            else :
                row_list = fft(Shaped_data/((data_time_lenght+1)/2))
                # Filter1 = 一定値以上を全てカット
                filter1_list = np.hstack((row_list[:filter_end],np.zeros(len(row_list)-filter_end)))
                # Filter2 = 一定範囲を除きカット
                filter2_list = np.hstack((np.zeros(filter_start), row_list[filter_start:filter_end],np.zeros(len(row_list)-filter_end)))
                #ax =  fig.add_subplot(8,12,i)
                if I == 1:
                    header = "Original plot"
                    period_plot_switch = 0
                    rfft_plot(ax, X_axis, Shaped_data, COLOR, Name, Subtitle, "", X_max, n_rythm)
                    
                elif I == 2 :
                    header = "Original fft plot"
                    period_plot_switch = 0
                    fft_plot(ax, X_axis, row_list, COLOR, Name, Subtitle,  X_max, n_rythm)
                    
                elif I == 3 :
                    header = "Reverse fft with r1_detector plot"
                    plot_data = np.real(np.fft.ifft(row_list*((data_time_lenght+1)/2)))
                    No_of_peak = " ({} ps)".format(range_1_local_max_detector(ax, X_axis, plot_data))
                    rfft_plot(ax, X_axis, plot_data, COLOR, Name, Subtitle, No_of_peak, X_max, n_rythm)

                elif I == 4 :
                    header = "Reverse fft with r2_detector plot"
                    plot_data = np.real(np.fft.ifft(row_list*((data_time_lenght+1)/2)))
                    No_of_peak = " ({} ps)".format(range_2_local_max_detector(ax, X_axis, plot_data))
                    rfft_plot(ax, X_axis, plot_data, COLOR, Name, Subtitle, No_of_peak, X_max, n_rythm)

                elif I == 5 :
                    header = "Reverse fft with r3_detector plot"
                    plot_data = np.real(np.fft.ifft(row_list*((data_time_lenght+1)/2)))
                    No_of_peak = " ({} ps)".format(range_3_local_max_detector(ax, X_axis, plot_data))
                    rfft_plot(ax, X_axis, plot_data, COLOR, Name, Subtitle, No_of_peak, X_max, n_rythm)

                elif I == 6 :
                    header = "Reverse fft with new_local_max_detector plot"
                    plot_data = np.real(np.fft.ifft(row_list*((data_time_lenght+1)/2)))
                    No_of_peak = " ({} ps)".format(new_local_max_detector(ax, X_axis, plot_data))
                    rfft_plot(ax, X_axis, plot_data, COLOR, Name, Subtitle, No_of_peak, X_max, n_rythm)

                else :
                    print("Skip")
                """
                elif I == 5 :
                    header = "Filter1_fft plot"
                    period_plot_switch = 0
                    fft_plot(ax, X_axis, filter1_list, COLOR, Name, Subtitle,  X_max, n_rythm)
                
                elif I == 6 :
                    header = "Reverse filter1_fft with r1_detector plot"
                    plot_data = np.real(np.fft.ifft(filter1_list*((data_time_lenght+1)/2)))
                    peak_info = range_1_local_max_detector(ax, X_axis, plot_data)
                    peak_time.append(peak_info[1])
                    No_of_peak = " ({} ps)".format(len(peak_info[1]))
                    rfft_plot(ax, X_axis, plot_data, COLOR, Name, Subtitle, No_of_peak, X_max, n_rythm)
                    
                elif I == 7 :
                    header = "Reverse filter1_fft with r3_detector plot"
                    plot_data = np.real(np.fft.ifft(filter1_list*((data_time_lenght+1)/2)))
                    peak_info = range_3_local_max_detector(ax, X_axis, plot_data)
                    peak_time.append(peak_info[1])
                    No_of_peak = " ({} ps)".format(len(peak_info[1]))
                    rfft_plot(ax, X_axis, plot_data, COLOR, Name, Subtitle, No_of_peak, X_max, n_rythm)
                
                elif I == 8:
                    header = "Filter2_fft plot"
                    period_plot_switch = 0
                    fft_plot(ax, X_axis, filter2_list, COLOR, Name, Subtitle,  X_max, n_rythm)
                
                elif I == 9 :
                    header = "Reverse filter2_fft with r1_detector plot"
                    plot_data = np.real(np.fft.ifft(filter2_list*((data_time_lenght+1)/2)))
                    peak_info = range_1_local_max_detector(ax, X_axis, plot_data)
                    peak_time.append(peak_info[1])
                    No_of_peak = " ({} ps)".format(len(peak_info[1]))
                    rfft_plot(ax, X_axis, plot_data, COLOR, Name, Subtitle, No_of_peak, X_max, n_rythm)
                    
                elif I == 10 :
                    header = "Reverse filter2_fft with r3_detector plot"
                    plot_data = np.real(np.fft.ifft(filter2_list*((data_time_lenght+1)/2)))
                    peak_info = range_3_local_max_detector(ax, X_axis, plot_data)
                    peak_time.append(peak_info[1])
                    No_of_peak = " ({} ps)".format(len(peak_info[1]))
                    rfft_plot(ax, X_axis, plot_data, COLOR, Name, Subtitle, No_of_peak, X_max, n_rythm)
                
                else :
                    print("skip")
                """

            ax.set_title('{0}{1} ({2})'.format(ROW, Col, Subtitle))
            ax.set_xticks(np.linspace(0, X_max, n_rythm+1)) # x 軸 (major) 目盛り設定
            ax.set_xticks(np.linspace(0, X_max, n_rythm*4+1), minor=True) # x 軸 (minor) 目盛り設定
            ax.grid(axis="both") #xy両方のグリットを表示

        Title = data_name + ' - ' + header
        fig.tight_layout()
        fig.suptitle(Title, fontsize=25)
        plt.subplots_adjust(top=0.95, left=0.05, bottom=0.08)
        fig.text(0.5, 0.02, 'frequency', ha='center', va='center', fontsize=15)
        fig.text(0.02, 0.5, 'amplitude', ha='center', va='center', rotation='vertical', fontsize=15)
        fig.align_labels()
        image_name = data_name
        plt.savefig( "{}.jpg".format(Title))
        #file_saver("96well(%)", "-", data_name, savefig_path)
        plt.show()


# Yaxis = ""
# all_plot(X_axis, new_data, data_ALL, data_name, savefig_path, Yaxis)
