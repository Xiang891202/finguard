"""統一回應包裝。"""
from typing import Any


def ok(data: Any = None, meta: dict | None = None) -> dict:
    """成功回應。"""
    payload: dict[str, Any] = {"success": True, "data": data}
    if meta is not None:
        payload["meta"] = meta
    return payload


def fail(
    code: str,
    message: str,
    details: dict | None = None,
) -> dict:
    """失敗回應（例外處理器用）。"""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        },
    }