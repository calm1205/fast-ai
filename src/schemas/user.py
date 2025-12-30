from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """ユーザー作成リクエスト"""

    name: str = Field(..., description="ユーザー名", min_length=1)
    email: str = Field(..., description="メールアドレス")


class UserUpdate(BaseModel):
    """ユーザー更新リクエスト"""

    name: str | None = Field(None, description="ユーザー名", min_length=1)
    email: str | None = Field(None, description="メールアドレス")


class UserResponse(BaseModel):
    """ユーザーレスポンス"""

    id: int = Field(..., description="ユーザーID")
    name: str = Field(..., description="ユーザー名")
    email: str = Field(..., description="メールアドレス")

    model_config = {"from_attributes": True}
