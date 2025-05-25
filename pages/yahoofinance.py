#!/usr/bin/env python
# coding: utf-8

# In[8]:


import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as  mticker
import matplotlib.font_manager as fm
import urllib.request

import pandas as pd
from datetime import datetime, timedelta
import platform


# In[ ]:


if platform.system() == 'Darwin':
    # macOS の場合
    font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
else:
    # Streamlit Cloud（Linux）などその他
    font_path = "pages/NotoSansCJK-Regular.ttc"

font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()


# In[ ]:


# import streamlit as st
# import yfinance as yf
# import matplotlib.pyplot as plt
# import matplotlib.ticker as mticker
# import pandas as pd
# from datetime import datetime, timedelta

# st.title("株価チャート：終値グラフ")

# # --- サイドバー入力 ---
# st.sidebar.header("オプション設定")

# # 銘柄コードの選択肢
# default_symbols = {
#     "日経平均（^N225）": "^N225",
#     "S&P 500（^GSPC）": "^GSPC",
#     "NASDAQ（^IXIC）": "^IXIC",
#     "Apple（AAPL）": "AAPL",
#     "Google（GOOG）": "GOOG",
#     "Microsoft（MSFT）": "MSFT",
#     "Tesla（TSLA）": "TSLA",
#     "ドル円（USD/JPY）": "JPY=X",  # ← これを追加
#     "その他（手動入力）": "custom"
# }

# symbol_choice = st.sidebar.selectbox("銘柄を選択", list(default_symbols.keys()))

# # 手動入力用テキストボックスの表示切替
# if default_symbols[symbol_choice] == "custom":
#     symbol = st.sidebar.text_input("銘柄コードを入力してください（例: 7203.T, META）", value="", key="custom_ticker")
# else:
#     symbol = default_symbols[symbol_choice]

# # period 選択
# period_options = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
# period = st.sidebar.selectbox("期間（period）", period_options)

# # interval 選択
# interval_options = ["1m", "5m", "15m", "30m", "60m", "90m", "1d", "5d", "1wk", "1mo", "3mo"]
# interval = st.sidebar.selectbox("間隔（interval）", interval_options)

# # 日付指定の切り替え
# use_custom_dates = st.sidebar.checkbox("日付を指定する（periodと併用不可）")

# # 開始日と終了日の入力（任意）
# start_date = None
# end_date = None
# if use_custom_dates:
#     start_date = st.sidebar.date_input("開始日", value=datetime.today() - timedelta(days=30))
#     end_date = st.sidebar.date_input("終了日", value=datetime.today())

# # --- データ取得関数 ---
# def download_stock_data(ticker, period="5d", interval="1d", start=None, end=None):
#     if start and end:
#         data = yf.download(ticker, start=start, end=end, interval=interval)
#     else:
#         data = yf.download(ticker, period=period, interval=interval)
#     return data

# # --- メイン画面 ---
# st.write(f"### 銘柄：{symbol}")

# try:
#     df = download_stock_data(
#         symbol,
#         period=period if not use_custom_dates else None,
#         interval=interval,
#         start=start_date if use_custom_dates else None,
#         end=end_date if use_custom_dates else None
#     )

#     if df.empty:
#         st.warning("データが取得できませんでした。銘柄コードや期間を確認してください。")
#     else:
#         # --- グラフ描画 ---
#         fig, ax = plt.subplots(figsize=(10, 5))
#         ax.plot(df.index, df["Close"], marker='o', linestyle='-', label="終値")
#         ax.set_title(f"{symbol} の終値", fontsize=14)
#         ax.set_xlabel("日付", fontsize=12)
#         ax.set_ylabel("終値", fontsize=12)
#         ax.grid(True)
#         ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
#         plt.xticks(rotation=45)
#         ax.legend()
#         st.pyplot(fig)

#         # データも表示
#         with st.expander("データ表示"):
#             st.dataframe(df)

# except Exception as e:
#     st.error(f"エラーが発生しました: {e}")


# In[ ]:


import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
from datetime import datetime, timedelta

st.title("株価・為替・金利チャート：終値表示")

# --- サイドバー入力 ---
st.sidebar.header("オプション設定")

# 銘柄コードの選択肢
default_symbols = {
    "日経平均（^N225）": "^N225",
    "S&P 500（^GSPC）": "^GSPC",
    "NASDAQ（^IXIC）": "^IXIC",
    "Apple（AAPL）": "AAPL",
    "Google（GOOG）": "GOOG",
    "Microsoft（MSFT）": "MSFT",
    "Tesla（TSLA）": "TSLA",
    "ドル円（USD/JPY）": "JPY=X",
    "米10年金利（^TNX）": "^TNX",
    "米2年金利（^IRX）": "^IRX",
    "その他（手動入力）": "custom"
}

symbol_choice = st.sidebar.selectbox("銘柄を選択", list(default_symbols.keys()))

# 手動入力か選択肢から取得
if default_symbols[symbol_choice] == "custom":
    symbol = st.sidebar.text_input("銘柄コードを入力（例: META, 7203.T）", value="", key="custom_ticker")
else:
    symbol = default_symbols[symbol_choice]

# period 選択
period_options = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
period = st.sidebar.selectbox("期間（period）", period_options)

# interval 選択
interval_options = ["1d", "5d", "1wk", "1mo", "3mo"]
interval = st.sidebar.selectbox("間隔（interval）", interval_options)

# 日付指定
use_custom_dates = st.sidebar.checkbox("日付を指定する（periodと併用不可）")
start_date, end_date = None, None
if use_custom_dates:
    start_date = st.sidebar.date_input("開始日", value=datetime.today() - timedelta(days=90))
    end_date = st.sidebar.date_input("終了日", value=datetime.today())

# --- データ取得関数 ---
def download_stock_data(ticker, period="5d", interval="1d", start=None, end=None):
    if start and end:
        return yf.download(ticker, start=start, end=end, interval=interval)
    else:
        return yf.download(ticker, period=period, interval=interval)

# --- メイン処理 ---
if symbol:
    st.write(f"### 終値チャート：{symbol}")

    try:
        df = download_stock_data(
            symbol,
            period=period if not use_custom_dates else None,
            interval=interval,
            start=start_date if use_custom_dates else None,
            end=end_date if use_custom_dates else None
        )

        if df.empty:
            st.warning("データが取得できませんでした。コードや期間を確認してください。")
        else:
            # 米国金利ティッカーの補正（値を10で割る）
            if symbol in ["^TNX", "^IRX", "^TYX"]:
                df["Close"] = df["Close"] / 10

            # グラフ描画
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df.index, df["Close"], marker='o', linestyle='-', label="終値")
            ax.set_title(f"{symbol} の終値チャート", fontsize=14, fontproperties=font_prop)
            ax.set_xlabel("日付", fontsize=12, fontproperties=font_prop)
            ax.set_ylabel("終値", fontsize=12, fontproperties=font_prop)
            ax.grid(True)
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.2f}"))
            plt.xticks(rotation=45)
            ax.legend()
            st.pyplot(fig)

            # データ表示
            with st.expander("データ表示"):
                st.dataframe(df)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
else:
    st.info("銘柄コードを入力または選択してください。")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


#
#  ＜＜＜ SNA.pyに変換 ＞＞＞
#

