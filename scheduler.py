import os
import sys
import time
import schedule
from core.logger import LOG  # 导入日志模块

# 导入核心模块和报告生成模块
from core.github_client import GitHubClient
from reports.report_generator import ReportGenerator
from core.llm import LLM
from config.configs import Config  # 导入配置管理模块

# 守护进程相关配置
PID_FILE = "github_sentinel_demon.pid"
STATUS_FILE = "logs/github_sentinel_demon_status.txt"
LOG_FILE = "logs/github_sentinel_demon.log"
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}"
# 初始化日志系统
# LOG.basicConfig(filename=LOG_FILE, level=LOG.INFO)
LOG.add(LOG_FILE, rotation="1 MB", level="DEBUG", format=LOG_FORMAT)

# 初始化 GitHubClient 实例
github_client = GitHubClient()
config = Config()
# 定时任务
def job():
    try:
        # 生成每日报告
        LOG.info("Starting to fetch updates and generate daily reports.")
        github_client.generate_report()
        LOG.info("Daily reports generated successfully.")

        # 生成最终总结报告
        LOG.info("Starting to generate final summarized report.")
        llm = LLM(config)
        report = ReportGenerator(llm)
        report.generate_final_report()
        LOG.info("Final summarized report generated successfully.")

        LOG.info("Scheduled job executed successfully at %s", time.strftime('%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        LOG.error(f"Error during scheduled job: {str(e)}")

# 守护进程相关功能

def is_running():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    return False

def write_status():
    with open(STATUS_FILE, "w") as f:
        f.write(f"Daemon running with PID {os.getpid()} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

def start_daemon():
    if is_running():
        print("Daemon is already running.")
        return

    # Fork一个子进程
    pid = os.fork()
    if pid > 0:
        # 父进程退出
        sys.exit(0)

    # 子进程继续运行
    os.setsid()
    os.umask(0)

    # 第二次fork，防止获得终端控制
    pid = os.fork()
    if pid > 0:
        sys.exit(0)

    # 重定向标准文件描述符
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'r') as dev_null:
        os.dup2(dev_null.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'a+') as dev_null:
        os.dup2(dev_null.fileno(), sys.stdout.fileno())
        os.dup2(dev_null.fileno(), sys.stderr.fileno())

    # 写入 PID 文件
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    LOG.info("Daemon started with PID %s", os.getpid())

    # 定时调度任务（例如每天早上9点执行）
    schedule_interval = "daily"  # 可以从配置文件读取
    if schedule_interval == "daily":
        schedule.every().day.at("09:00").do(job)
    elif schedule_interval == "weekly":
        schedule.every().monday.at("09:00").do(job)
    else:
        # 默认每小时执行一次
        schedule.every().hour.do(job)

    try:
        while True:
            schedule.run_pending()
            write_status()
            LOG.info("Heartbeat at %s", time.strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(60)
    except Exception as e:
        LOG.error(f"Daemon encountered an error: {str(e)}")
    finally:
        stop_daemon(clean=False)

def stop_daemon(clean=True):
    if not os.path.exists(PID_FILE):
        print("Daemon is not running.")
        return
    with open(PID_FILE, "r") as f:
        pid = int(f.read().strip())
    try:
        os.kill(pid, 15)  # 发送终止信号
        if clean:
            os.remove(PID_FILE)
            LOG.info("Daemon was manually stopped.")
        print(f"Daemon with PID {pid} has been stopped.")
    except OSError as e:
        print(f"Error stopping daemon: {str(e)}")

def check_status():
    if is_running():
        with open(STATUS_FILE, "r") as f:
            print(f.read())
    else:
        print("Daemon is not running.")

def view_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            print(f.read())
    else:
        print("No logs found.")

# CLI 功能用于管理守护进程
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: scheduler.py [start|stop|status|logs]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "start":
        print("Starting daemon...")
        start_daemon()
    elif command == "stop":
        print("Stopping daemon...")
        stop_daemon()
    elif command == "status":
        print("Checking daemon status...")
        check_status()
    elif command == "logs":
        print("Viewing logs...")
        view_logs()
    else:
        print("Unknown command. Use start, stop, status, or logs.")