from typing import List, Optional
from pydantic import BaseModel, Field


# Google APIs用のレスポンススキーマ（詳細）
class TokenDetail(BaseModel):
    """トークンの詳細情報"""

    modality: str = Field(..., description="モダリティタイプ（TEXT等）")
    tokenCount: int = Field(..., description="トークン数")


class UsageMetadata(BaseModel):
    """使用量メタデータ"""

    promptTokenCount: int = Field(..., description="プロンプトのトークン数")
    candidatesTokenCount: int = Field(..., description="候補のトークン数")
    totalTokenCount: int = Field(..., description="総トークン数")
    promptTokensDetails: List[TokenDetail] = Field(
        ..., description="プロンプトトークンの詳細"
    )
    candidatesTokensDetails: List[TokenDetail] = Field(
        ..., description="候補トークンの詳細"
    )


class ContentPart(BaseModel):
    """コンテンツの一部"""

    text: str = Field(..., description="生成されたテキスト")


class Content(BaseModel):
    """コンテンツ情報"""

    parts: List[ContentPart] = Field(..., description="コンテンツの部分")
    role: str = Field(..., description="ロール（model等）")


class Candidate(BaseModel):
    """候補の情報"""

    content: Content = Field(..., description="コンテンツ")
    finishReason: str = Field(..., description="終了理由")
    avgLogprobs: Optional[float] = Field(None, description="平均対数確率")


class GeminiFullResponse(BaseModel):
    """Gemini APIの完全なレスポンス"""

    candidates: List[Candidate] = Field(..., description="候補のリスト")
    usageMetadata: UsageMetadata = Field(..., description="使用量メタデータ")
    modelVersion: str = Field(..., description="モデルバージョン")
    responseId: str = Field(..., description="レスポンスID")


class GeminiRequest(BaseModel):
    """Gemini APIのリクエストスキーマ"""

    prompt: str = Field(..., description="プロンプトを入力してください", min_length=1)


class GeminiResponse(BaseModel):
    """Gemini APIのレスポンススキーマ"""

    prompt: str = Field(..., description="元のプロンプト")
    response: str = Field(..., description="生成されたテキスト")
    # full_response: GeminiFullResponse = Field(..., description="完全なAPIレスポンス")
