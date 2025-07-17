import pandas as pd
import matplotlib.pyplot as plt
import os

def compute_daily_active_wallets(df: pd.DataFrame) -> pd.DataFrame:
    df["blockTime"] = pd.to_datetime(df["blockTime"])
    df["date"] = df["blockTime"].dt.date
    daily_active = {}

    for _, row in df.iterrows():
        date = row["date"]
        for wallet in row["accountKeys"]:
            daily_active.setdefault(date, set()).add(wallet)

    df_daily = pd.DataFrame([
        {"date": date, "active_wallets": len(wallets)}
        for date, wallets in daily_active.items()
    ])
    df_daily = df_daily.sort_values("date")
    return df_daily

def plot_active_wallets(df_daily: pd.DataFrame, save_path: str = "figures/active_wallets.png"):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_daily["date"], df_daily["active_wallets"], marker="o", label="活躍錢包數")
    ax.set_xlabel("日期")
    ax.set_ylabel("活躍錢包數")
    ax.set_title("Solana 每日活躍錢包數")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path)
        print(f"✅ 活躍錢包圖已儲存：{save_path}")
    return fig
