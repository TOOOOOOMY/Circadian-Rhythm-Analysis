!pip install xlrd


import os
import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import itertools

# 測定結果読み込み
def data_reader(file_name, file_location = "/content/"): # remane -> main?
    file_type = file_name.split(".")[-1]
    # print(file_type)
    if file_type == "csv":
        return aloka_reader(file_location, file_name)
    elif file_type == "xlsx":
        return lumicec_reader(file_location, file_name)
    else :
        print("Error : Please use csv or xlsx file.")
        return None


# 96well positions 読み込み
def well_positions_reader(file_name = "96well_positions.csv", file_location = "/content/"):
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
        print("エラー：該当するファイル名のファイルが見つかりません。")
        return None


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


def percentage_cal(data):
    new_data = pd.DataFrame(columns=data.columns.values)
    for col in data.columns.values:
        new_data[col] = data[col]/max(data[col])*100
    return new_data


def col_posi_linker(col_name, positions):
    if col_name[1] == "0":
        return positions.at[col_name[0], col_name[2]]
    else :
        return positions.at[col_name[0], col_name[1:3]]

