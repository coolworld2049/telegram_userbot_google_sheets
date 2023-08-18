from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

from settings import settings

api_key = APIKeyHeader(name="api_key", auto_error=False)


async def verify_api_key(key: str = Depends(api_key)):
    if key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
