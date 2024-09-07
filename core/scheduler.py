# core/scheduler.py

import schedule
import time
import threading
from core.updater import fetch_updates
from core.notifier import notify
from reports.report_generator import ReportGenerator

def job():
    updates = fetch_updates()
    report = ReportGenerator.generate_final_report(updates)
    # notify(report)

def start_scheduler():
    schedule_interval = "daily"  # 这里可以从配置文件读取
    if schedule_interval == "daily":
        schedule.every().day.at("09:00").do(job)
    elif schedule_interval == "weekly":
        schedule.every().monday.at("09:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler_in_background():
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.daemon = True  # 使线程在主程序退出时自动结束
    scheduler_thread.start()
