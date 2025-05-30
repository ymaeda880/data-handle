#!/usr/bin/env python
# coding: utf-8

# In[1]:


#
# SNAデータの表示とグラフ描画
#

import streamlit as st
import pandas as pd

import re
import subprocess
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm
import urllib.request
import platform
#import japanize_matplotlib

#plt.rcParams['font.family'] = 'Hiragino Sans'
#plt.rcParams['font.family'] = 'Noto Sans CJK JP'


# In[ ]:


def open_by_excel(df, file_name = 'out', folder_path='../MacroData/SNA/',
            sheet_name='データ'):
    file_name = file_name+'.xlsx'
    file_path = folder_path + file_name
    # Excel に保存
    df.to_excel(file_path, index=True, sheet_name=sheet_name)
    # ファイルを開く（Mac: 'open' / Windows: 'start' / Linux: 'xdg-open'）
    subprocess.run(['open', file_path])


# In[2]:


#
# 環境設定
#

folder_path='/Users/macmini2025/myVenv/DataAnalysis/MacroData/SNA/'

# sw_local = False
# if sw_local:
#     folder_path='../MacroData/SNA/'
# else:
#     folder_path='MacroData/SNA/'

file_name = 'SNA_data.csv'


# この page のみで run するか？
# runしない場合は SNA.py のみを作成
sw_run = True
#sw_run = False


if platform.system() == 'Darwin':
    # macOS の場合
    font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
    file_path = folder_path+file_name
else:
    # Streamlit Cloud（Linux）などその他
    font_path = "pages/NotoSansCJK-Regular.ttc"
    file_path = "https://ymaeda.jp/data/"+file_name

font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

#font_prop = fm.FontProperties(fname="NotoSansCJK-Regular.ttc")
#plt.rcParams['font.family'] = font_prop.get_name()


# In[ ]:





# In[8]:


#
# データの読み込み
#

# file_name = 'SNA_data.csv'

# if sw_data == 'server':
#     url = "https://ymaeda.jp/data/"+file_name
#     df = pd.read_csv(file_path, index_col=0, encoding='utf-8-sig')
# else:
#     file_path=folder_path+file_name
#     df = pd.read_csv(file_path, index_col=0, encoding='utf-8-sig')

df = pd.read_csv(file_path, index_col=0, encoding='utf-8-sig')
df.columns = df.columns.astype(str)    


# In[3]:


#df.columns
#df.head()


# In[ ]:


#
# streamlit（開始）
#

st.title("SNAデータのグラフを描画")
st.dataframe(df)  # インタラクティブな表形式で表示（スクロールや並べ替えが可能）

# 項目リストを表示（複数選択可）
selected_items = st.multiselect("表示する項目を選んでください", df.index.tolist())


# In[ ]:


#
# ボタンで描画実行
#

if st.button("グラフを描画"):
    if not selected_items:
        st.warning("少なくとも1つの項目を選んでください。")
    else:
        st.subheader("選択項目の時系列グラフ")
        fig, ax = plt.subplots()
        for item in selected_items:
            ax.plot(df.columns, df.loc[item], label=item, marker='o')
        ax.set_xlabel("年", fontproperties=font_prop)
        ax.set_ylabel("値", fontproperties=font_prop)
        ax.set_title("選択した項目の推移", fontproperties=font_prop)
        ax.legend(prop=font_prop)
        ax.grid(True)

        # ✅ 年のラベルが重ならないように回転と位置調整
        plt.xticks(rotation=50, ha='right')

        # ✅ Y軸に3桁カンマを追加
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

        st.pyplot(fig)


# In[ ]:





# In[ ]:





# In[5]:


#
#  ＜＜＜ SNA.pyに変換 ＞＞＞
#

