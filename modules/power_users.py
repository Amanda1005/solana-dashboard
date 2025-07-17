import pandas as pd
import matplotlib.pyplot as plt
import os

def extract_top_wallets(df: pd.DataFrame, top_n=10) -> pd.DataFrame:
    wallet_counter = {}

    for _, row in df.iterrows():
        for wallet in row["accountKeys"]:
            wallet_counter[wallet] = wallet_counter.get(wallet, 0) + 1

    df_top = pd.DataFrame([
        {"wallet": wallet, "tx_count": count}
        for wallet, count in wallet_counter.items()
    ])
    df_top = df_top.sort_values("tx_count", ascending=False).head(top_n).reset_index(drop=True)
    return df_top

def plot_top_wallets(df_top: pd.DataFrame, save_path: str = "figures/top_wallets.png"):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df_top["wallet"], df_top["tx_count"], color="skyblue")
    ax.set_xlabel("交易次數")
    ax.set_title("Top 活躍用戶（依交易次數）")
    ax.invert_yaxis()
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path)
        print(f"✅ Top 錫包排行圖已儲存：{save_path}")
    return fig