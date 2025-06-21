from typing import List
from pydantic import BaseModel, Field


# Google APIs用のリクエストスキーマ
class GeminiAPIPartRequest(BaseModel):
    """Gemini APIのpart要素"""

    text: str = Field(..., description="送信するテキスト")


class GeminiAPIContentRequest(BaseModel):
    """Gemini APIのcontent要素"""

    parts: List[GeminiAPIPartRequest] = Field(..., description="partsのリスト")


class GeminiAPIRequest(BaseModel):
    """Google Gemini APIへの実際のリクエストボディ"""

    contents: List[GeminiAPIContentRequest] = Field(..., description="contentsのリスト")

    @classmethod
    def from_prompt(cls, prompt: str) -> "GeminiAPIRequest":
        """プロンプトからAPIリクエストを生成するヘルパーメソッド"""
        return cls(
            contents=[
                GeminiAPIContentRequest(parts=[GeminiAPIPartRequest(text=prompt)])
            ]
        )
