import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import os

def build_retention_matrix(df: pd.DataFrame, max_days: int = 7) -> pd.DataFrame:
    df["blockTime"] = pd.to_datetime(df["blockTime"])
    df["date"] = df["blockTime"].dt.date

    # 展開所有 wallet 與交易日期
    records = []
    for _, row in df.iterrows():
        for wallet in row["accountKeys"]:
            records.append({
                "wallet": wallet,
                "date": row["date"]
            })
    all_wallets = pd.DataFrame(records)

    # 找每個 wallet 第一次出現的日期
    first_seen = all_wallets.groupby("wallet")["date"].min().reset_index()
    first_seen.columns = ["wallet", "first_date"]

    # 合併進來
    all_wallets = all_wallets.merge(first_seen, on="wallet")
    all_wallets["days_since_first"] = (
        pd.to_datetime(all_wallets["date"]) - pd.to_datetime(all_wallets["first_date"])
    ).dt.days
    all_wallets = all_wallets[all_wallets["days_since_first"] <= max_days]

    # 留存矩陣：index 為 first_date，columns 為 Day N
    cohort = all_wallets.groupby(["first_date", "days_since_first"])["wallet"].nunique().unstack(fill_value=0)
    cohort = cohort.div(cohort[0], axis=0)  # 換算為比例
    return cohort.round(3)

def plot_retention_heatmap(retention_df: pd.DataFrame, save_path="figures/retention_heatmap.png"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(retention_df, annot=True, fmt=".0%", cmap="Blues", cbar=False, ax=ax)
    ax.set_title("用戶留存率（Retention Heatmap）")
    ax.set_xlabel("Day")
    ax.set_ylabel("首次互動日 (Cohort)")
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path)
        print(f"✅ 留存熱力圖已儲存：{save_path}")
    return fig

if __name__ == "__main__":
    wallet_prefix = "MJKqp3"
    input_path = f"data/{wallet_prefix}_normalized.csv"
    output_fig = f"figures/{wallet_prefix}_retention_heatmap.png"

    df = pd.read_csv(input_path, converters={"accountKeys": ast.literal_eval})
    retention_df = build_retention_matrix(df, max_days=6)
    print("📊 留存分析結果：")
    print(retention_df)

    fig = plot_retention_heatmap(retention_df, save_path=output_fig)
    plt.show()
