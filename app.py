# 📈 SmartTrade Signal AI - Final Version
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import ta

st.set_page_config(page_title="SmartTrade Signal AI", layout="centered")

st.title("📊 SmartTrade Signal AI")
st.write("Get Buy/Sell Signals using RSI, MACD, and Moving Averages")

# Input
symbol = st.text_input("Enter Stock Symbol (e.g., TCS.NS, RELIANCE.NS)", "RELIANCE.NS")
start_date = st.date_input("Start Date", datetime.today() - timedelta(days=180))
end_date = st.date_input("End Date", datetime.today())

if st.button("🔍 Analyze"):
    try:
        df = yf.download(symbol, start=start_date, end=end_date)

        if df.empty:
            st.error("❌ No data found. Check the symbol.")
        else:
            st.success("✅ Data Loaded")

            # Indicators using 'ta'
            df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
            macd = ta.trend.MACD(df['Close'])
            df['MACD'] = macd.macd()
            df['Signal'] = macd.macd_signal()
            df['MA50'] = ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator()
            df['MA200'] = ta.trend.SMAIndicator(df['Close'], window=200).sma_indicator()

            latest = df.iloc[-1]

            # Indicator Values
            st.subheader("📈 Latest Indicators:")
            st.write(f"**RSI**: {latest['RSI']:.2f}")
            st.write(f"**MACD**: {latest['MACD']:.2f}")
            st.write(f"**Signal Line**: {latest['Signal']:.2f}")
            st.write(f"**MA50**: {latest['MA50']:.2f}")
            st.write(f"**MA200**: {latest['MA200']:.2f}")

            # Signal Logic
            st.subheader("📌 Recommendation")
            signal = "Hold"

            if latest['RSI'] < 30 and latest['MACD'] > latest['Signal'] and latest['Close'] > latest['MA50']:
                signal = "✅ Strong Buy"
            elif latest['RSI'] > 70 and latest['MACD'] < latest['Signal'] and latest['Close'] < latest['MA50']:
                signal = "❌ Strong Sell"

            st.markdown(f"### 🔔 Signal: **{signal}**")

            # Chart
            st.line_chart(df[['Close', 'MA50', 'MA200']].dropna())

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
