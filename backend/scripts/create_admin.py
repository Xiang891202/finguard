"""CLI：建立 / 更新管理員帳號。

用法（在 backend/ 目錄）：
    python scripts/create_admin.py --email ah891202@gmail.com --password 'ah891202'
"""
import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.user import AdminUser


async def main() -> int:
    parser = argparse.ArgumentParser(description="建立 FinGuard 管理員")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--name", default="管理員")
    args = parser.parse_args()

    if len(args.password) < 6:
        print("密碼至少 6 字元")
        return 1
    if len(args.password.encode("utf-8")) > 72:
        print("密碼過長（bcrypt 上限 72 bytes）")
        return 1

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(AdminUser).where(AdminUser.email == args.email)
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.password_hash = hash_password(args.password)
            print(f"✅ 已更新管理員密碼：{args.email}")
        else:
            session.add(AdminUser(
                email=args.email,
                password_hash=hash_password(args.password),
                display_name=args.name,
                role="admin",
                status="active",
            ))
            print(f"✅ 已建立管理員：{args.email}")

        await session.commit()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))