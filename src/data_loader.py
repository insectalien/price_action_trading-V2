import os
import pandas as pd
import requests

def get_data():
    file_path = "data/tsmc_2330.csv"
    
    # 檢查 data 資料夾是否存在
    if not os.path.exists("data"):
        os.makedirs("data")

    # 如果檔案存在，直接讀取
    if os.path.exists(file_path):
        print("Reading from local CSV...")
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date']) # 強制轉成日期格式
        return df
    
    # 如果檔案不存在，才抓 API 並存檔
    else:
        print("Fetching from API...")
    # 從FinMind抓取（台股 2330 台積電）
    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
        "dataset": "TaiwanStockPrice",
        "data_id": "2330",
        "start_date": "2024-01-01"
    }
    response = requests.get(url, params=parameter)
    
    # 把得到的 JSON 格式轉成 Pandas 的表格 (DataFrame)
    df = pd.DataFrame(response.json()["data"])
    df['date'] = pd.to_datetime(df['date']) # 存檔前也先轉好
    df.to_csv(file_path, index=False) # 存成 CSV 備用
    return df