import os
from dotenv import load_dotenv
from typing import Optional

# 環境変数を読み込み
load_dotenv()


def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    環境変数を取得する

    Args:
        key: 環境変数のキー
        default: デフォルト値（指定されていない場合はNone）

    Returns:
        環境変数の値またはデフォルト値
    """
    return os.getenv(key, default)


def get_required_env_var(key: str) -> str:
    """
    必須の環境変数を取得する

    Args:
        key: 環境変数のキー

    Returns:
        環境変数の値

    Raises:
        ValueError: 環境変数が設定されていない場合
    """
    value = os.getenv(key)
    if not value:
        raise ValueError(f"{key} environment variable is not set")
    return value
