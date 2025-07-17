import requests
import json
import time
import os
import random

# 🧮 範例地址：可換成你要分析的錢包地址
wallet_address = "MJKqp326RZCHnAAbew9MDdui3iCKWco7fsK9sVuZTX2"

solana_rpc = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}

def safe_post(body, retries=3):
    for i in range(retries):
        try:
            resp = requests.post(solana_rpc, headers=headers, json=body, timeout=10)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"⚠️ 第{i+1}次嘗試失敗：{e}")
            time.sleep(random.uniform(1, 3))
    return {}

def get_signatures(address, limit=50, before=None):
    params = {"limit": limit}
    if before:
        params["before"] = before
    body = {
        "jsonrpc": "2.0", "id": 1,
        "method": "getSignaturesForAddress",
        "params": [address, params]
    }
    result = safe_post(body)
    return result.get("result", [])

def get_transaction(signature):
    body = {
        "jsonrpc": "2.0", "id": 1,
        "method": "getTransaction",
        "params": [signature, {"encoding": "json"}]
    }
    result = safe_post(body)
    return result.get("result")

def fetch_transactions_for_wallet(address, max_pages=2, per_page=30):
    all_txs, before, seen = [], None, set()
    for page in range(max_pages):
        print(f"\n📄 第 {page+1} 頁 signatures 抓取中...")
        sigs = get_signatures(address, limit=per_page, before=before)
        if not sigs:
            print("❌ 沒有拿到更多 signatures，停止抓取")
            break

        for item in sigs:
            sig = item["signature"]
            if sig in seen:
                continue
            seen.add(sig)

            print(f"⏳ 抓取交易 {sig}")
            tx = get_transaction(sig)
            if tx:
                all_txs.append(tx)

        before = sigs[-1]["signature"]
        time.sleep(0.3)
    return all_txs

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    short_addr = wallet_address[:6]
    output_path = f"data/{short_addr}_transactions.json"

    txs = fetch_transactions_for_wallet(wallet_address, max_pages=5, per_page=30)
    with open(output_path, "w") as f:
        json.dump(txs, f)

    print(f"\n✅ 抓取完成！共取得 {len(txs)} 筆交易資料，已儲存至：{output_path}")

    # 示範讀取前幾筆資料
    print("\n📦 第一筆交易資料預覽：")
    print(json.dumps(txs[0], indent=2) if txs else "沒有資料")
