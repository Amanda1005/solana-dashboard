import pandas as pd
import ast
import os
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def extract_wallet_features(df: pd.DataFrame) -> pd.DataFrame:
    wallet_stats = {}

    for _, row in df.iterrows():
        date = pd.to_datetime(row["blockTime"]).date()
        for wallet in row["accountKeys"]:
            if wallet not in wallet_stats:
                wallet_stats[wallet] = {
                    "tx_count": 0,
                    "active_days": set(),
                    "contracts": set()
                }
            wallet_stats[wallet]["tx_count"] += 1
            wallet_stats[wallet]["active_days"].add(date)
            wallet_stats[wallet]["contracts"].update(row["programIds"])

    rows = []
    for wallet, stats in wallet_stats.items():
        rows.append({
            "wallet": wallet,
            "tx_count": stats["tx_count"],
            "active_days": len(stats["active_days"]),
            "used_contracts": len(stats["contracts"])
        })

    df_features = pd.DataFrame(rows)
    if df_features.empty:
        print("⚠️ 沒有錢包互動資料可分析。")
    return df_features

def run_clustering(df_features: pd.DataFrame, n_clusters=3) -> pd.DataFrame:
    if len(df_features) < n_clusters:
        print(f"⚠️ 錢包數過少（{len(df_features)}），無法執行 {n_clusters} 分群")
        df_features["cluster"] = 0  # 全部分為同一群
        return df_features

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    features = df_features[["tx_count", "active_days", "used_contracts"]]
    df_features["cluster"] = kmeans.fit_predict(features)
    return df_features

def plot_clusters(df: pd.DataFrame, save_path="figures/user_segments.png"):
    if df.empty:
        print("⚠️ 無法繪圖：用戶特徵資料為空。")
        return None

    plt.figure(figsize=(8, 6))
    for cluster_id in sorted(df["cluster"].unique()):
        subset = df[df["cluster"] == cluster_id]
        plt.scatter(subset["tx_count"], subset["active_days"], label=f"群組 {cluster_id}", alpha=0.7)
    
    plt.xlabel("交易次數")
    plt.ylabel("活躍天數")
    plt.title("用戶分群圖（交易次數 vs 活躍天數）")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"✅ 分群圖已儲存：{save_path}")
    plt.show()
    return plt.gcf()

if __name__ == "__main__":
    wallet_prefix = "MJKqp3"
    input_path = f"data/{wallet_prefix}_normalized.csv"
    output_csv = f"data/{wallet_prefix}_user_segments.csv"
    output_fig = f"figures/{wallet_prefix}_user_segments.png"

    df = pd.read_csv(input_path, converters={"accountKeys": ast.literal_eval, "programIds": ast.literal_eval})
    features_df = extract_wallet_features(df)
    if not features_df.empty:
        features_df = run_clustering(features_df, n_clusters=3)
        features_df.to_csv(output_csv, index=False)
        print(f"✅ 分群分析完成，已儲存至：{output_csv}")
        print(features_df.head())
        plot_clusters(features_df, save_path=output_fig)
    else:
        print("⛔ 資料為空，跳過分群與繪圖。")
