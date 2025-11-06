from fastapi import FastAPI, Depends
from authtuna import init_app
from authtuna.integrations import get_current_user_optional, RoleChecker
from authtuna.core.database import User
from fastapi.responses import RedirectResponse
from authtuna.integrations import auth_service
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await auth_service.roles.get_or_create("member", {"description": "Default member role", "level": 0})
    await auth_service.roles.get_or_create("domain_lead", {"description": "Domain Lead role", "level": 0})
    await auth_service.roles.grant_relationship("domain_lead", "member", auth_service.roles, "can_assign_roles")
    user = (await auth_service.users.get_by_username("Ishaan"))
    if user:
        await auth_service.roles.assign_to_user(user.id, "member", "system")
        await auth_service.roles.assign_to_user(user.id, "domain_lead", "system")
    yield

app = FastAPI(lifespan=lifespan)

init_app(app)

@app.get("/", tags=["Root"],)
async def root(user: User=Depends(get_current_user_optional)):
    """
    Automatically redirects to login page if not authenticated, else redirects to the dashboard.
    """
    if user is None:
        return RedirectResponse("/auth/login")
    return RedirectResponse("/ui/dashboard")

@app.get("/domain-lead-area", tags=["Domain Lead Area"], dependencies=[Depends(RoleChecker("domain_lead"))])
async def domain_lead_area():
    """
    An example endpoint that only domain leads can access.
    """
    return {"message": "Welcome to the Domain Lead area!"}

@app.get("/member-area", tags=["Member Area"], dependencies=[Depends(RoleChecker("member"))])
async def domain_lead_area():
    """
    An example endpoint that members can access.
    """
    return {"message": "Welcome to the Member area!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5000, host="0.0.0.0")
