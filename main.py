from src.data_loader import get_data 
from src.strategy import apply_engulfing_strategy
from src.visualizer import plot_signals
from src.backtester import Backtester  
import logging  # 1. 導入日誌庫

# 2. 設定日誌：同時輸出到螢幕與檔案
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("trading_system.log"), # 存成檔案
        logging.StreamHandler()                    # 顯示在螢幕
    ]
)

def run_trading_system():
    logging.info("Step 1: 正在抓取市場數據...")
    df_raw = get_data()
    
    logging.info("Step 2: 正在執行策略分析...")
    df_analyzed = apply_engulfing_strategy(df_raw)
    
    # 3. 初始化回測器
    bt = Backtester(df_analyzed)
    
    # --- 實驗區：停損參數測試 ---
    logging.info("正在執行停損參數實驗...")
    for sl_value in [0.01, 0.03, 0.05, 0.08, 0.10]:
        report = bt.run_advanced(stop_loss=sl_value, take_profit=0.10)
        # 這裡要加一個判斷，避免沒交易時噴錯
        if "Total Trades" in report:
            print(f"停損設為 {sl_value*100:>2.0f}% | 勝率: {report['Win Rate']} | 總報酬: {report['Cumulative Return']}")
    print("-----------------------\n")

    # 4. 執行一組「你最終決定」的參數做為正式報告
    print("Step 3: Running Final Backtest Report...")
    stats = bt.run_advanced(take_profit=0.05, stop_loss=0.1)

    # 5. 輸出結果統計
    num_bull = df_analyzed['bull_signal'].sum()
    print(f"Analysis Complete: Found {num_bull} Buy signals.")
    print("\n--- Final Strategy Performance Report ---")
    for key, value in stats.items():
        print(f"{key}: {value}")
    print("-----------------------------------\n")
    
    # 6. 視覺化
    logging.info("Step 4: 生成視覺化圖表...")
    plot_signals(df_analyzed)

if __name__ == "__main__":
    try:
        run_trading_system()
    except Exception as e:
        print(f"❌ 程式執行發生錯誤：{e}", exc_info=True)  # 紀錄錯誤細節