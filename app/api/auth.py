from fastapi import APIRouter, HTTPException
router=APIRouter(prefix="/auth",tags=["Auth"])
@router.post("/demo-login")
def demo_login(username:str):
    if not username: raise HTTPException(400,"Username required")
    return {"message":"Demo authentication only","username":username}
