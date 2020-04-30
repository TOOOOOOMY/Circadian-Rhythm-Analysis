"""
更新最新情報：
200109 - グラフの軸表記設定を追加
"""

#使い方
##０-１：左上にある「Playgroundで開く」をクリック

##０-２：左上にある「＞」をクリック

##１：「目次」「コードスニペット」「ファイル」のうち「ファイル」をクリック
##　（「ファイルのブラウジング～」との表示が出ている場合は、自動で起動するまでしばらく待つ　or　上のタブから「ランタイム」→「ランタイムを再起動」）

##２：「アップロード」から解析したいファイル（csv形式）をアップロード（「注：アップロードした～」の警告にはOKをクリック）

##３：下の「"」に囲まれた部分をアップロードしたファイル名（拡張子除く）に変更、例：sample.cvsをアップロードした場合は"sample"とする
##　　　　ファイル形式に関してはこちらを参照→https://sites.google.com/view/pythonforchlamy/csv-files
file_name = "sample1"  

##４-１：サンプリング周期を分単位で入力（下のsampling_period = xxのxxを変える、以下同じ）
sampling_period = 60

##４-２：予測される周期を時間単位で入力（不明な場合はそのまま）
estimated_period = 24

##５：Overview plotの有無を入力（無→０、有→１）
over_view_plot_switch = 1

##６：All plotの有無を選択（無→０、有→１）
all_plot_switch = 1

##７：Shiftキーを押しながらEnterキーを押す（＝プログラムが実行されます）

##８：「データ名＋グラフ名.jpg」の画像ファイルが左「ファイル」欄に生成されるまで待つ（待ち時間は通信状況等により変化します）

##９：画像ファイルを右クリック→ダウンロード




"""
＝＝＝＝＝＝＝＝＝＝
簡易設定（グラフ関係）
"""
##x軸単位（「"」に囲まれた部分を書き換え、以下同じ）
x_axis_title = "Time [h]"
##y軸単位
y_axis_title = "Bioluminescence"

##Overview plotでのグラフ横列表示数（１～５、標準３）
column_number = 3

##All plotでのグラフ間Y軸共有の有無（共有無→０、有→１）
y_axis_share_switch = 1

##グループ番号毎の色（参考：https://matplotlib.org/examples/color/named_colors.html）、先頭から数字の０に対応
color_list = ["black", "red", "orange", "green", "lightgreen", "blue", "lightblue", "yellow", "teal", "cyan",  "gray"]

##グループ番号毎のタイトル、先頭から数字の０に対応
subtitle_list = ["Group0", "Resi", "Group2", "Sens", "Group4", "Group5", "Group6", "Group7", "Group8", "Group9", "Group10"]

"""
＝＝＝＝＝＝＝＝＝＝
"""


"""
＝＝＝＝＝＝＝＝＝＝
詳細設定
"""
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
＝＝＝＝＝＝＝＝＝＝
"""


"""
==========
ここから下はいじらない
==========

Author: Tomoki WATANABE
Update: 11/01/2020
Version: 2.0
License: BSD License
Programing Language: Python3

"""
import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.fftpack import fft


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


def router(file_name, y_axis_switch, over_view_plot_switch, all_plot_switch, color_list, subtitle_list, column_number):
    row_data = pd.read_csv("/content/{0}.csv".format(file_name), engine="python", encoding="utf-8_sig")
    try:
        new_data = row_data.drop('Unnamed: 0', axis=1).T
        X_axis = round(row_data["Unnamed: 0"].iloc[1:].reset_index(drop=True).astype(float), 4)
    except KeyError:
        new_data = row_data.drop('Time', axis=1).T
        X_axis = round(row_data['Time'].iloc[1:].reset_index(drop=True).astype(float), 4)
    finally:
        try:
            all_data = new_data.drop(0, axis=1).T.reset_index(drop=True)
            data_name = file_name
        except:
            print("<==========\nCSV file Error. \n\nA1 cell needs to be 'Time' or blank.\n==========>")
            sys.exit()
        else:
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
        #変数セット
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
    for i in range(1, new_data.shape[0]+1):
        ax =  fig.add_subplot(-(-new_data.shape[0]//a_column),a_column,i)

        ROW, Col = well_namer(i)

        Name = '{0}{1}'.format(ROW, Col)
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


router(file_name, y_axis_share_switch, over_view_plot_switch, all_plot_switch, color_list, subtitle_list, column_number)
