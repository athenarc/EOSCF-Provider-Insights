from fastapi import Header, HTTPException
from settings import APP_SETTINGS


def verify_access_token(x_access_token: str = Header(default=None)):
    if x_access_token is None:
        raise HTTPException(status_code=401, detail="x-access-token header missing")
    if x_access_token != APP_SETTINGS["CREDENTIALS"]["ACCESS_TOKEN"]:
        raise HTTPException(status_code=401, detail="x-access-token header invalid")
