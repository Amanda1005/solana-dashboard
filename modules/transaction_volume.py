import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["blockTime"] = pd.to_datetime(df["blockTime"])
    df["date"] = df["blockTime"].dt.date
    return df

def compute_transaction_volume(df: pd.DataFrame) -> pd.DataFrame:
    df["blockTime"] = pd.to_datetime(df["blockTime"])
    df["date"] = df["blockTime"].dt.date
    daily = df.groupby("date").agg(
        total_transactions=("signature", "count"),
        total_fee=("fee", "sum"),
        success_rate=("success", "mean")
    ).reset_index()
    return daily

def plot_transaction_volume(daily_df: pd.DataFrame, save_path: str = "figures/transaction_volume.png"):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(daily_df["date"], daily_df["total_transactions"], marker='o', label="交易筆數")
    ax.plot(daily_df["date"], daily_df["total_fee"], marker='s', label="總手續費")
    ax.set_xlabel("日期")
    ax.set_ylabel("數量")
    ax.set_title("Solana 每日交易筆數與總手續費")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path)
        print(f"✅ 圖表已儲存為：{save_path}")
    return fig

if __name__ == "__main__":
    wallet_prefix = "MJKqp3"
    input_path = f"data/{wallet_prefix}_normalized.csv"
    output_csv = f"data/{wallet_prefix}_transaction_volume.csv"
    output_fig = f"figures/{wallet_prefix}_transaction_volume.png"

    df = load_data(input_path)
    daily_df = compute_transaction_volume(df)
    daily_df.to_csv(output_csv, index=False)

    print(f"✅ 每日交易量分析已完成，共 {len(daily_df)} 天，資料儲存至：{output_csv}")
    print(daily_df.head())

    plot_transaction_volume(daily_df, save_path=output_fig)