import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ast

from modules.active_wallets import compute_daily_active_wallets, plot_active_wallets
from modules.transaction_volume import compute_transaction_volume, plot_transaction_volume
from modules.power_users import extract_top_wallets, plot_top_wallets
from modules.user_segmentation import extract_wallet_features, run_clustering, plot_clusters

wallet_prefix = "MJKqp3"
data_path = f"data/{wallet_prefix}_normalized.csv"

st.set_page_config(page_title="Solana Web3 Dashboard", layout="wide")
st.title("📊 Solana Web3 用戶行為分析 Dashboard")

st.markdown("""
這個儀表板整合來自 Solana 上指定錢包的交易資料，呈現用戶活躍度、交易模式與用戶輪廓，適合用於：
- 🔎 行為分析
- 📈 商業決策參考
- 🧪 面試作品展示
""")

st.sidebar.image("https://s3.coinmarketcap.com/static-gravity/image/5cc0b99a8dd84fbfa4e150d84b5531f2.png", width=120)
st.sidebar.markdown("## 分析選單")

# 載入資料
df = pd.read_csv(data_path, converters={"accountKeys": ast.literal_eval, "programIds": ast.literal_eval})

# 分頁選單
page = st.sidebar.radio("請選擇分析模組 👇", [
    "每日活躍錢包",
    "交易量與手續費趨勢",
    "高頻用戶排行",
    "用戶分群分析"
])

if page == "每日活躍錢包":
    st.subheader("📅 每日活躍錢包")
    st.markdown("每一天中至少發出 1 筆交易的錢包數量")
    df_daily = compute_daily_active_wallets(df)
    fig = plot_active_wallets(df_daily, save_path=None)
    st.pyplot(fig)
    with st.expander("👉 查看原始數據表格"):
        st.dataframe(df_daily)

elif page == "交易量與手續費趨勢":
    st.subheader("📈 每日交易量與手續費")
    st.markdown("包含每日的交易總數、手續費總額與成功率")
    df_tx = compute_transaction_volume(df)
    fig2 = plot_transaction_volume(df_tx, save_path=None)
    st.pyplot(fig2)
    with st.expander("👉 查看原始數據表格"):
        st.dataframe(df_tx)

elif page == "高頻用戶排行":
    st.subheader("🏆 高頻用戶排行")
    st.markdown("根據交易次數，列出出現最頻繁的用戶地址")
    df_top = extract_top_wallets(df, top_n=10)
    fig3 = plot_top_wallets(df_top, save_path=None)
    st.pyplot(fig3)
    with st.expander("👉 查看原始數據表格"):
        st.dataframe(df_top)

elif page == "用戶分群分析":
    st.subheader("🔍 用戶分群分析 (KMeans)")
    st.markdown("根據交易次數、活躍天數、使用合約數進行用戶聚類")
    features_df = extract_wallet_features(df)
    clustered_df = run_clustering(features_df, n_clusters=3)
    fig4 = plot_clusters(clustered_df, save_path=None)
    st.pyplot(fig4)
    with st.expander("👉 查看原始數據表格"):
        st.dataframe(clustered_df.head())

st.markdown("---")
st.markdown("👩‍💻 Made by Amanda | Powered by Python + Streamlit")