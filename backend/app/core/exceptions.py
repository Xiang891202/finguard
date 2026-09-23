from fastapi import HTTPException, status

class FinGuardException(HTTPException):
    def __init__(self, code: str, message: str, status_code: int = 400):
        super().__init__(
            status_code=status_code,
            detail={"code": code, "message": message}
        )

class NotFoundError(FinGuardException):
    def __init__(self, resource: str):
        super().__init__("NOT_FOUND", f"{resource} 不存在", 404)

class UnauthorizedError(FinGuardException):
    def __init__(self, message: str = "未授權"):
        super().__init__("UNAUTHORIZED", message, 401)