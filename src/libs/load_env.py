import os
from dotenv import load_dotenv
from typing import Optional

# 環境変数を読み込み
load_dotenv()


def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    """環境変数を取得する"""
    return os.getenv(key, default)


def get_required_env_var(key: str) -> str:
    """必須の環境変数を取得する"""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"{key} environment variable is not set")
    return value
