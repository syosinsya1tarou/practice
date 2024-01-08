import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from sklearn.linear_model import LinearRegression
import datetime

st.title("売上予測") # タイトル

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください") # ファイルアップロード

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['日付'] = pd.to_datetime(df['日付']) # 日付列をdatetime型に変換
    min_date = df['日付'].min()
    max_date = df['日付'].max()

    # 日付の範囲を選択
    selected_date = st.date_input('日付を選択してください', [min_date, max_date])

    # 選択した日付の範囲のデータを抽出
    mask = (df['日付'] >= pd.to_datetime(selected_date[0])) & (df['日付'] <= pd.to_datetime(selected_date[1]))

    df_selected = df.loc[mask]

    if df_selected.empty:
        st.write('日付が無効です。再選択してください')
    else:
        X = df_selected.iloc[:, 2:-1] # 説明変数
        y = df_selected.iloc[:, 1] # 目的変数（売上）

        # 線形回帰モデルを作成
        model = LinearRegression()
        model.fit(X, y)

        # 予測値を計算
        y_pred = model.predict(X)

        # グラフを描画
        plt.figure(figsize=(12, 6))
        plt.plot(df_selected['日付'], y, label='実績')
        plt.plot(df_selected['日付'], y_pred, label='予測')
        plt.title('売上予測')
        plt.xlabel('日付')
        plt.ylabel('売上（千円）')
        plt.legend()
        st.pyplot(plt)
else:
    st.write("CSVファイルをアップロードしてください")
