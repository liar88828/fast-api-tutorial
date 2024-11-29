from fastapi import HTTPException, Request


# Middleware function to verify the access token
async def verify_access_token(request: Request, call_next):
    token = request.headers.get("Authorization")
    if not token or token != "Bearer valid_access_token":
        raise HTTPException(status_code=401, detail="Invalid or missing access token")
    response = await call_next(request)
    return response


# Dependency to check access token
async def verify_token_dependency(request: Request):
    token = request.headers.get("Authorization")
    if not token or token != "Bearer valid_access_token":
        raise HTTPException(status_code=401, detail="Invalid or missing access token")
    return token

# Dependency to check access token
