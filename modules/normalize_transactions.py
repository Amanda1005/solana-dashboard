import json
import pandas as pd
from typing import Dict
import os

def extract_transaction_fields(tx: Dict) -> Dict:
    return {
        "signature": tx.get("transaction", {}).get("signatures", [None])[0],
        "blockTime": tx.get("blockTime"),
        "slot": tx.get("slot"),
        "fee": tx.get("meta", {}).get("fee"),
        "err": tx.get("meta", {}).get("err"),
        "success": tx.get("meta", {}).get("err") is None,
        "programIds": [ix.get("programId") for ix in tx.get("transaction", {}).get("message", {}).get("instructions", [])],
        "accountKeys": tx.get("transaction", {}).get("message", {}).get("accountKeys", []),
    }

def normalize_transactions(json_path: str) -> pd.DataFrame:
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"❌ 找不到檔案：{json_path}")
    
    with open(json_path, "r") as f:
        raw_data = json.load(f)
    
    records = [extract_transaction_fields(tx) for tx in raw_data]
    df = pd.DataFrame(records)
    
    # 轉換時間格式
    if "blockTime" in df.columns:
        df["blockTime"] = pd.to_datetime(df["blockTime"], unit="s")

    return df

if __name__ == "__main__":
    wallet_prefix = "MJKqp3"  # 根據妳的錢包前綴碼（檔名）設定
    input_path = f"data/{wallet_prefix}_transactions.json"
    output_path = f"data/{wallet_prefix}_normalized.csv"

    df = normalize_transactions(input_path)
    df.to_csv(output_path, index=False)

    print(f"✅ 資料清洗完成，共 {len(df)} 筆交易，儲存為 {output_path}")
    print(df.head(3))
