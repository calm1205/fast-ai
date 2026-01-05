import json
import sqlite3
from typing import Any

from fastapi import APIRouter, HTTPException
import httpx

from src.libs.load_env import get_required_env_var
from src.schemas.gemini import GeminiResponse, GeminiRequest
from src.schemas.google import (
    GeminiAPIContentRequest,
    GeminiAPIPartRequest,
    Tool,
    FunctionDeclaration,
    FunctionParameter,
)

router = APIRouter()

DB_PATH = "data/app.db"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent"

# search_usersツールの定義
SEARCH_USERS_TOOL = Tool(
    function_declarations=[
        FunctionDeclaration(
            name="search_users",
            description="Search users by name or email (partial match)",
            parameters=FunctionParameter(
                type="object",
                properties={
                    "query": {
                        "type": "string",
                        "description": "Search query for name or email",
                    }
                },
                required=["query"],
            ),
        )
    ]
)


def search_users_from_db(query: str) -> list[dict[str, Any]]:
    """DBからユーザーを検索"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email FROM users WHERE name LIKE ? OR email LIKE ?",
        (f"%{query}%", f"%{query}%"),
    )
    rows = cursor.fetchall()
    conn.close()

    return [{"id": row["id"], "name": row["name"], "email": row["email"]} for row in rows]


async def call_gemini_api(
    api_key: str,
    contents: list[GeminiAPIContentRequest],
    tools: list[Tool] | None = None,
) -> dict[str, Any]:
    """Gemini APIを呼び出す"""
    url = f"{GEMINI_API_URL}?key={api_key}"

    request_body: dict[str, Any] = {"contents": [c.model_dump() for c in contents]}
    if tools:
        request_body["tools"] = [t.model_dump() for t in tools]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=request_body,
            headers={"Content-Type": "application/json"},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


@router.post("/gemini", response_model=GeminiResponse)
async def gemini(request: GeminiRequest) -> GeminiResponse:
    """
    Gemini APIを呼び出してテキストを生成します。
    """
    api_key = get_required_env_var("GEMINI_API_KEY")

    contents = [GeminiAPIContentRequest(parts=[GeminiAPIPartRequest(text=request.prompt)])]

    try:
        result = await call_gemini_api(api_key, contents)

        if "candidates" in result and len(result["candidates"]) > 0:
            generated_text = result["candidates"][0]["content"]["parts"][0]["text"]
            return GeminiResponse(prompt=request.prompt, response=generated_text)

        return GeminiResponse(prompt=request.prompt, response="レスポンスの生成に失敗しました")

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Gemini API error: {e.response.text}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/gemini/user/search", response_model=GeminiResponse)
async def gemini_user_search(request: GeminiRequest) -> GeminiResponse:
    """
    Gemini APIのFunction Callingを使用してユーザーを検索します。
    自然文でユーザー検索ができます。
    """
    api_key = get_required_env_var("GEMINI_API_KEY")

    contents = [GeminiAPIContentRequest(parts=[GeminiAPIPartRequest(text=request.prompt)])]

    try:
        # 1. ツール付きでGemini APIを呼び出し
        result = await call_gemini_api(api_key, contents, tools=[SEARCH_USERS_TOOL])

        if "candidates" not in result or len(result["candidates"]) == 0:
            return GeminiResponse(prompt=request.prompt, response="レスポンスの生成に失敗しました")

        candidate = result["candidates"][0]
        parts = candidate["content"]["parts"]

        # 2. Function Callがあるかチェック
        function_call = None
        for part in parts:
            if "functionCall" in part:
                function_call = part["functionCall"]
                break

        # Function Callがない場合は通常のテキストレスポンス
        if not function_call:
            text = parts[0].get("text", "レスポンスの生成に失敗しました")
            return GeminiResponse(prompt=request.prompt, response=text)

        # 3. Function Callを実行
        func_name = function_call["name"]
        func_args = function_call["args"]

        if func_name == "search_users":
            search_result = search_users_from_db(func_args["query"])
        else:
            search_result = {"error": f"Unknown function: {func_name}"}

        # 4. 結果をGeminiに返して最終回答を生成
        contents.append(
            GeminiAPIContentRequest(
                parts=[GeminiAPIPartRequest(text=json.dumps(candidate["content"]))]
            )
        )
        contents.append(
            GeminiAPIContentRequest(
                parts=[
                    GeminiAPIPartRequest(
                        text=json.dumps(
                            {
                                "functionResponse": {
                                    "name": func_name,
                                    "response": {"result": search_result},
                                }
                            }
                        )
                    )
                ]
            )
        )

        final_result = await call_gemini_api(api_key, contents)

        if "candidates" in final_result and len(final_result["candidates"]) > 0:
            final_text = final_result["candidates"][0]["content"]["parts"][0].get(
                "text", "レスポンスの生成に失敗しました"
            )
            return GeminiResponse(prompt=request.prompt, response=final_text)

        return GeminiResponse(prompt=request.prompt, response="レスポンスの生成に失敗しました")

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Gemini API error: {e.response.text}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
