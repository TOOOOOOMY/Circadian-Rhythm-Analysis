# 概日リズム解析パッケージ「cr-analysis」
**README in English is available from [here](https://github.com/TOOOOOOMY/Circadian-Rhythm-Analysis).**  
概日リズム解析において、測定データをグラフ化して大まかに比較できるパッケージです。  
プログラムミングはよくわからないという人向けに、Googleアカウントとインターネット環境を利用した3行でできる解析方法も記載しています。詳しくは本ページ下部の「プログラムミングはよくわからない方へ」を参照してください。  
  
なお、本パッケージは「とりあえずグラフ化して測定結果の概要を見たい」といった予備解析的な場合での利用を想定しています。  

## 使用例
```py
pip install cr-analysis
from cr_analysis.main import visualizer

# Prepare the csv file. E.g. sample1.csv
# E.g. 
visualizer('sample1.csv', file_path = '/content/drive/My Drive/')
```

１：概要＆同系列を重ねて表示
![sample1 csv - overview_4_col_plot](https://user-images.githubusercontent.com/45617592/86256856-c680d380-bbf3-11ea-92a7-92be3bdb547f.jpg)

  
２：個別に表示
![sample1 csv - All_plot](https://user-images.githubusercontent.com/45617592/86256927-d993a380-bbf3-11ea-9a42-b81b4fc07ff8.jpg)


３：重ね合わせて表示
![sample1 csv - comparison_plot](https://user-images.githubusercontent.com/45617592/86256644-8883af80-bbf3-11ea-8c4b-38d8090bbffd.png)

## 特徴
・３行のコピペで上記使用例のような解析が可能です。  
・解析速度はインターネット環境や解析ファイルサイズによりますが、97列x150行のデータであれば30秒ほどで完了します。  

## 
