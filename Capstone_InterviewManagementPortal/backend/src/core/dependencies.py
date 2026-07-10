from fastapi import Request, HTTPException

def get_current_user(request: Request):
   
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

def require_role(required_roles: list):
    
    def role_checker(request: Request):
        user = get_current_user(request)
        role = user.get("role")
        if role not in required_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Role '{role}' not allowed. Required: {required_roles}"
            )
        return user
    return role_checker