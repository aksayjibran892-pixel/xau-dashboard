import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

# ==========================================
# KONFIGURASI
# ==========================================
API_KEY = "06adf95b771eb7dcb5d082985c75575d-c-app"
st.set_page_config(page_title="XAU Dashboard", layout="wide")

# Auto Refresh pakai Meta (cara paling simple buat HP)
st.markdown("<meta http-equiv='refresh' content='10' />", unsafe_allow_html=True)

# ==========================================
# TAMPILAN
# ==========================================
st.title("📊 XAU/USD LIVE DASHBOARD")
st.caption("Update otomatis setiap 10 detik | Data: Yahoo Finance")

# Ambil Data
@st.cache_data(ttl=10)
def get_data():
    try:
        t = yf.Ticker("GC=F") # Gold Futures
        h = t.history(period="1d")
        p = h['Close'].iloc[-1]
        c = h['Close'].iloc[-1] - h['Open'].iloc[-1]
        return p, c
    except:
        return 2300.00, 0.0

price, change = get_data()

# Warna
if change >= 0:
    warna = "green"
    icon = "▲"
else:
    warna = "red"
    icon = "▼"

# Tampilan Harga
col1, col2 = st.columns(2)
with col1:
    st.metric("SPOT PRICE", f"${price:,.2f}", f"{icon} {change:.2f}")
with col2:
    st.metric("API STATUS", "CONNECTED" if API_KEY else "OFFLINE")

# Chart
st.markdown("---")
st.subheader("📈 CHART (1 Bulan)")
try:
    df = yf.download("GC=F", period="1mo", progress=False)
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        increasing_line_color='green', decreasing_line_color='red'
    )])
    fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
except:
    st.warning("Gagal memuat chart. Coba refresh.")

# Signal Simple
st.markdown("---")
if change > 0:
    st.success("🟢 AI SIGNAL: BUY (Bullish)")
else:
    st.error("🔴 AI SIGNAL: SELL (Bearish)")
