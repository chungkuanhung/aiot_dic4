import streamlit as st
import sqlite3
import pandas as pd
import time
import altair as alt

DB_NAME = "aiotdb.db"

st.set_page_config(page_title="IoT 即時溫濕度監控", layout="wide")
st.title("🌡️ 即時溫濕度監測系統")
st.markdown("本系統會動態從 `aiotdb.db` 中讀取資料並畫出即時溫濕度圖表。")

# 建立圖表與資料表格的 UI 佔位符
chart_placeholder = st.empty()
data_placeholder = st.empty()

def get_data():
    """從資料庫讀取最新的感測器資料"""
    try:
        conn = sqlite3.connect(DB_NAME)
        # 3. 從 aiotdb.db query 出資料 (取得最近的 60 筆做即時顯示)
        query = "SELECT timestamp, temperature, humidity FROM sensors ORDER BY id DESC LIMIT 60"
        df = pd.read_sql(query, conn)
        conn.close()
        
        if not df.empty:
            # 將資料時序反轉，畫圖時舊資料在左、新資料在右
            df = df.iloc[::-1].reset_index(drop=True)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            # 將 timestamp 設為 index 給 st.line_chart 直接繪製
            df.set_index('timestamp', inplace=True)
            
            # 更換一下欄位名稱讓圖表 legend 更直觀
            df.rename(columns={'temperature': '溫度 (°C)', 'humidity': '濕度 (%)'}, inplace=True)
        return df
    except Exception as e:
        # 資料庫可能尚未建立、表格不存在，或遭遇 DatabaseError
        return pd.DataFrame()

# 3. 使用無窮迴圈每隔一段時間查詢資料並動態繪製圖表
while True:
    df = get_data()
    
    if not df.empty:
        # 畫出 (dynamic) 即時線圖 (雙 Y 軸)
        with chart_placeholder.container():
            st.subheader("📊 即時溫濕度趨勢圖")
            df_plot = df.reset_index()
            # 建立基底圖
            base = alt.Chart(df_plot).encode(x=alt.X('timestamp:T', title='時間'))
            
            # 左邊的 Y 軸：溫度
            line_temp = base.mark_line(color='#ff2b2b').encode(
                y=alt.Y('溫度 (°C):Q', title='溫度 (℃)', axis=alt.Axis(titleColor='#ff2b2b'))
            )
            # 右邊的 Y 軸：濕度
            line_hum = base.mark_line(color='#0068c9').encode(
                y=alt.Y('濕度 (%):Q', title='濕度 (%)', axis=alt.Axis(titleColor='#0068c9'))
            )
            
            # 將兩條線疊加並設定各自獨立的 Y 軸
            chart = alt.layer(line_temp, line_hum).resolve_scale(y='independent')
            st.altair_chart(chart, use_container_width=True)
            
        # 顯示原始資料列表幫助確認
        with data_placeholder.container():
            st.subheader("📋 最近寫入紀錄")
            # 排序讓最新的在最上方顯示
            st.dataframe(df.sort_index(ascending=False).head(10), use_container_width=True)
    else:
        chart_placeholder.info("⏳ 資料庫尚未準備好或無資料，請先運行 `generate_data.py` 背景寫入。")
        
    time.sleep(2)  # 每 2 秒刷新一次查詢與圖表 (配合寫入頻率)
