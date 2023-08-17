from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyQuery

from settings import settings

api_key = APIKeyQuery(name="api_key")


async def verify_api_key(key: str = Depends(api_key)):
    if key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
