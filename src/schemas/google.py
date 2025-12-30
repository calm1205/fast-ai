from typing import Any
from pydantic import BaseModel, Field


# Google APIs用のリクエストスキーマ
class GeminiAPIPartRequest(BaseModel):
    """Gemini APIのpart要素"""

    text: str = Field(..., description="送信するテキスト")


class GeminiAPIContentRequest(BaseModel):
    """Gemini APIのcontent要素"""

    parts: list[GeminiAPIPartRequest] = Field(..., description="partsのリスト")


class FunctionParameter(BaseModel):
    """Function Callingのパラメータ定義"""

    type: str = "object"
    properties: dict[str, Any] = Field(default_factory=dict)
    required: list[str] = Field(default_factory=list)


class FunctionDeclaration(BaseModel):
    """Function Callingの関数定義"""

    name: str
    description: str
    parameters: FunctionParameter


class Tool(BaseModel):
    """Gemini APIのツール定義"""

    function_declarations: list[FunctionDeclaration]


class GeminiAPIRequest(BaseModel):
    """Google Gemini APIへの実際のリクエストボディ"""

    contents: list[GeminiAPIContentRequest] = Field(..., description="contentsのリスト")
    tools: list[Tool] | None = None

    @classmethod
    def from_prompt(cls, prompt: str, tools: list[Tool] | None = None) -> "GeminiAPIRequest":
        """プロンプトからAPIリクエストを生成するヘルパーメソッド"""
        return cls(
            contents=[
                GeminiAPIContentRequest(parts=[GeminiAPIPartRequest(text=prompt)])
            ],
            tools=tools,
        )
