import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_active_wallets(csv_path: str,
                        save_path: str = "figures/active_wallets_trend.png",
                        show_plot: bool = True,
                        save_fig: bool = True):
    # 讀取資料
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # 計算移動平均
    df["ma_3"] = df["active_wallets"].rolling(window=3).mean()
    df["ma_7"] = df["active_wallets"].rolling(window=7).mean()

    # 繪製圖表
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["date"], df["active_wallets"], label="每日活躍錢包", marker='o', linewidth=2)
    ax.plot(df["date"], df["ma_3"], label="3日平均", linestyle='--')
    ax.plot(df["date"], df["ma_7"], label="7日平均", linestyle=':')
    ax.set_xlabel("日期")
    ax.set_ylabel("活躍錢包數")
    ax.set_title("Solana 每日活躍錢包趨勢圖")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    # 儲存圖表
    if save_fig:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path)
        print(f"✅ 圖表已儲存為：{save_path}")

    # 顯示圖表
    if show_plot:
        plt.show()

    return fig  # 回傳給 Streamlit 用

if __name__ == "__main__":
    csv_path = "data/MJKqp3_daily_active_wallets.csv"
    plot_active_wallets(csv_path)
