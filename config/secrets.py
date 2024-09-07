# config/secrets.py

# 在这里存储API密钥等敏感信息

import os

# 从系统环境变量读取 GitHub Token
GITHUB_TOKEN = os.getenv("GITHUB_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# print(OPENAI_API_KEY)

# 如果没有设置环境变量则抛出错误
if not GITHUB_TOKEN:
    raise EnvironmentError("Environment variable GITHUB_KEY not found. Please set it before running the application.")