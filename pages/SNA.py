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


# In[3]:


#
# 環境設定
#

folder_path='MacroData/SNA/'
file_name = 'SNA_data.csv'

# データの場所
#sw_data = 'local'
sw_data = 'server'


# この page のみで run するか？
# runしない場合は SNA.py のみを作成
sw_run = True
#sw_run = False

plt.rcParams['font.family'] = 'Hiragino Sans'



# In[4]:


def open_by_excel(df, file_name = 'out', folder_path='MacroData/SNA/',
            sheet_name='データ'):
    file_name = file_name+'.xlsx'
    file_path = folder_path + file_name
    # Excel に保存
    df.to_excel(file_path, index=True, sheet_name=sheet_name)
    # ファイルを開く（Mac: 'open' / Windows: 'start' / Linux: 'xdg-open'）
    subprocess.run(['open', file_path])


# In[ ]:





# In[16]:


#
# データの読み込み
#

file_name = 'SNA_data.csv'

if sw_data == 'server':
    url = "https://ymaeda.jp/data/"+file_name
    df = pd.read_csv(url, index_col=0, encoding='utf-8-sig')
else:
    file_path=folder_path+file_name
    df = pd.read_csv(file_path, index_col=0, encoding='utf-8-sig')

df.columns = df.columns.astype(str)    


# In[18]:


#df.head()


# In[ ]:


#
# streamlit（開始）
#

st.title("SNAデータのグラフを描画")
st.dataframe(df)  # インタラクティブな表形式で表示（スクロールや並べ替えが可能）

# 項目リストを表示（複数選択可）
selected_items = st.multiselect("表示する項目を選んでください", df.index.tolist())


# In[8]:


#
# フォントの選択
#

# === フォント定義（名前、URL、ファイル名） ===
FONT_CANDIDATES = {
    "Hiragino":{},
    "Noto Sans CJK JP": {
        "url": "https://github.com/googlefonts/noto-cjk/blob/main/Sans/OTC/NotoSansCJK-Regular.ttc?raw=true",
        "filename": "NotoSansCJK-Regular.ttc"
    },
    "IPAexGothic": {
        "url": "https://moji.or.jp/wp-content/ipafont/IPAexfont/IPAexGothic/IPAexGothic.ttf",
        "filename": "IPAexGothic.ttf"
    }
}

# === ボタン選択インターフェース ===
st.subheader("フォントを選んでください")

selected_font = None
for name in FONT_CANDIDATES:
    if st.button(name):
        selected_font = name
        st.write('選択されたフォント：',name)


if selected_font:
    if selected_font == 'Hiragino':
        plt.rcParams['font.family'] = 'Hiragino Sans'
        st.success("Hiraginoフォントを使用しました（mac限定）")
    else:
        font_info = FONT_CANDIDATES[selected_font]
        font_path = font_info["filename"]
        st.write(font_info)

        # === フォントをローカルに保存（なければDL） ===
        if not os.path.exists(font_path):
            with st.spinner(f"{selected_font} をダウンロード中..."):
                urllib.request.urlretrieve(font_info["url"], font_path)

        # === matplotlib に適用 ===
        font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
        st.success(f"{selected_font} フォントを適用しました")





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
        ax.set_xlabel("年")
        ax.set_ylabel("値")
        ax.set_title("選択した項目の推移")
        ax.legend()
        ax.grid(True)

        # ✅ 年のラベルが重ならないように回転と位置調整
        plt.xticks(rotation=50, ha='right')

        # ✅ Y軸に3桁カンマを追加
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

        st.pyplot(fig)


# In[ ]:





# In[ ]:





# In[ ]:


#
#  ＜＜＜ SNA.pyに変換 ＞＞＞
#

