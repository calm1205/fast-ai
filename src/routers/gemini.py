from fastapi import APIRouter, HTTPException
import httpx
from src.libs.load_env import get_required_env_var
from src.schemas.gemini import GeminiResponse, GeminiRequest
from src.schemas.google import GeminiAPIRequest


router = APIRouter()


@router.post("/gemini", response_model=GeminiResponse)
async def gemini(request: GeminiRequest) -> GeminiResponse:
    """
    Gemini APIを呼び出してテキストを生成します
    """
    # 環境変数からAPI keyを取得
    api_key = get_required_env_var("GEMINI_API_KEY")

    # Gemini APIのURL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    # Google APIs用のリクエストスキーマを使用してリクエストボディを作成
    api_request = GeminiAPIRequest.from_prompt(request.prompt)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=api_request.model_dump(),
                headers={"Content-Type": "application/json"},
                timeout=30.0,
            )
            response.raise_for_status()

            result = response.json()

            # レスポンスから生成されたテキストを抽出
            if "candidates" in result and len(result["candidates"]) > 0:
                generated_text = result["candidates"][0]["content"]["parts"][0]["text"]
                return GeminiResponse(
                    prompt=request.prompt,
                    response=generated_text,
                    # full_response=result
                )
            else:
                return GeminiResponse(
                    prompt=request.prompt,
                    response="レスポンスの生成に失敗しました",
                    # full_response=result,
                )

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Gemini API error: {e.response.text}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
