from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional
from datetime import timedelta
from contextlib import asynccontextmanager
from .database import database, metadata, engine
from . import crud
from .schemas import (
    PublicComponentCreate, PublicComponentUpdate, TeamComponentCreate, 
    TeamComponentUpdate, TeamImageUpdate, UserCreate, UserLogin, Token, User
)
from .auth import (
    authenticate_user, create_access_token, get_current_active_user, 
    get_password_hash, check_team_access, ACCESS_TOKEN_EXPIRE_MINUTES
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    metadata.create_all(bind=engine)
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(
    title="FRC Components API", 
    description="A public API for managing FRC robot components and team inventories",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["System"])
async def root():
    return {"message": "FRC Components API is running!"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_svg = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='0.9em' font-size='90'>🤖</text></svg>"""
    return Response(content=favicon_svg, media_type="image/svg+xml")

# === AUTHENTICATION ===

@app.post("/register", response_model=dict, tags=["Authentication"])
async def register_user(user: UserCreate):
    existing_user = await crud.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    existing_email = await crud.get_user_by_email(user.email)
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "team_id": user.team_id,
        "role": "member",
        "is_active": True
    }
    
    user_id = await crud.create_user(user_data)
    return {
        "id": user_id,
        "message": f"User {user.username} registered successfully",
        "username": user.username,
        "team_id": user.team_id
    }

@app.post("/token", response_model=Token, tags=["Authentication"])
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User, tags=["Authentication"])
async def read_users_me(current_user = Depends(get_current_active_user)):
    return User(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        team_id=current_user.team_id,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )

# === PUBLIC COMPONENTS ===

@app.post("/public-components/", tags=["Public Components"])
async def create_public_component(component: PublicComponentCreate):
    try:
        await crud.create_public_component(component.model_dump())
        return {"id": component.id, "message": "Component created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/public-components/", tags=["Public Components"])
async def get_public_components():
    components = await crud.get_all_public_components()
    return [dict(component) for component in components]

@app.get("/public-components/search", tags=["Public Components"])
async def search_public_components(
    q: Optional[str] = Query(None, description="Search in name, description, and ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    vendor: Optional[str] = Query(None, description="Filter by vendor"),
    min_cost: Optional[float] = Query(None, description="Minimum cost"),
    max_cost: Optional[float] = Query(None, description="Maximum cost"),
    availability: Optional[str] = Query(None, description="Filter by availability status"),
    has_cad_files: Optional[bool] = Query(None, description="Filter components with CAD files"),
    has_images: Optional[bool] = Query(None, description="Filter components with images")
):
    components = await crud.search_public_components(
        q, category, vendor, min_cost, max_cost, availability, has_cad_files, has_images
    )
    return [dict(component) for component in components]

@app.get("/public-components/{component_id}", tags=["Public Components"])
async def get_public_component(component_id: str):
    component = await crud.get_public_component(component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    return dict(component)

@app.put("/public-components/{component_id}", tags=["Public Components"])
async def update_public_component(component_id: str, component: PublicComponentUpdate):
    if not await crud.get_public_component(component_id):
        raise HTTPException(status_code=404, detail="Component not found")
    
    if not await crud.update_public_component(component_id, component.model_dump()):
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    return {"message": "Component updated successfully"}

@app.delete("/public-components/{component_id}", tags=["Public Components"])
async def delete_public_component(component_id: str):
    if not await crud.delete_public_component(component_id):
        raise HTTPException(status_code=404, detail="Component not found")
    return {"message": "Component deleted successfully"}

# === TEAM COMPONENTS ===

@app.post("/team-components/", tags=["Team Components"])
async def create_team_component(component: TeamComponentCreate,current_user = Depends(get_current_active_user)):
    check_team_access(current_user, component.team_id)
    
    try:
        component_id = await crud.create_team_component(component.model_dump())
        return {"id": component_id, "message": "Team component created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/teams/{team_id}/components", tags=["Team Components"])
async def get_team_components(team_id: str,current_user = Depends(get_current_active_user)):
    check_team_access(current_user, team_id)
    
    components = await crud.get_team_components(team_id)
    return [dict(component) for component in components]

@app.get("/team-components/{component_id}", tags=["Team Components"])
async def get_team_component(component_id: int,current_user = Depends(get_current_active_user)):
    component = await crud.get_team_component(component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Team component not found")
    check_team_access(current_user, component.team_id)
    
    return dict(component)

@app.put("/team-components/{component_id}", tags=["Team Components"])
async def update_team_component(component_id: int,component: TeamComponentUpdate,current_user = Depends(get_current_active_user)):
    existing_component = await crud.get_team_component(component_id)
    if not existing_component:
        raise HTTPException(status_code=404, detail="Team component not found")
    check_team_access(current_user, existing_component.team_id)
    
    if not await crud.update_team_component(component_id, component.model_dump()):
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    return {"message": "Team component updated successfully"}

@app.delete("/team-components/{component_id}", tags=["Team Components"])
async def delete_team_component(component_id: int,current_user = Depends(get_current_active_user)):
    existing_component = await crud.get_team_component(component_id)
    if not existing_component:
        raise HTTPException(status_code=404, detail="Team component not found")
    check_team_access(current_user, existing_component.team_id)
    
    if not await crud.delete_team_component(component_id):
        raise HTTPException(status_code=500, detail="Failed to delete team component")
    
    return {"message": "Team component deleted successfully"}

@app.post("/teams/{team_id}/components/{component_id}/add-image", tags=["Team Images"])
async def add_image_to_team_component(team_id: str, component_id: int, image_data: TeamImageUpdate, current_user = Depends(get_current_active_user)):
    check_team_access(current_user, team_id)
    
    component = await crud.get_team_component(component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Team component not found")
    if component.team_id != team_id:
        raise HTTPException(status_code=403, detail="Component does not belong to this team")
    success = await crud.update_team_component_image(component_id, image_data.image_url)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update component image")
    return {
        "message": "Image URL added to team component successfully",
        "team_id": team_id,
        "component_id": component_id,
        "image_url": image_data.image_url
    }

@app.post("/teams/{team_id}/add-image", tags=["Team Images"])
async def add_general_team_image(team_id: str, image_data: TeamImageUpdate, current_user = Depends(get_current_active_user)):
    check_team_access(current_user, team_id)
    
    image_id = await crud.create_team_image(team_id, image_data.image_url, image_data.description)
    return {
        "message": "Team image URL added successfully",
        "team_id": team_id,
        "image_id": image_id,
        "image_url": image_data.image_url
    }

# === UTILITY ENDPOINTS ===

@app.get("/categories", tags=["Utilities"])
async def get_categories():
    return await crud.get_categories()

@app.get("/vendors", tags=["Utilities"])
async def get_vendors():
    return await crud.get_vendors()

@app.get("/availability-statuses", tags=["Utilities"])
async def get_availability_statuses():
    return await crud.get_availability_statuses()

@app.get("/components/with-cad-files", tags=["Utilities"])
async def get_components_with_cad_files():
    components = await crud.get_components_with_cad_files()
    return [dict(component) for component in components]

@app.get("/components/with-images", tags=["Utilities"])
async def get_components_with_images():
    components = await crud.get_components_with_images()
    return [dict(component) for component in components]

@app.get("/teams/{team_id}/components/with-cad-files", tags=["Team Utilities"])
async def get_team_components_with_cad_files(team_id: str):
    components = await crud.get_team_components_with_cad_files(team_id)
    return [dict(component) for component in components]

@app.get("/teams/{team_id}/components/with-images", tags=["Team Utilities"])
async def get_team_components_with_images(team_id: str):
    components = await crud.get_team_components_with_images(team_id)
    return [dict(component) for component in components]

@app.get("/teams/{team_id}/inventory/summary", tags=["Team Utilities"])
async def get_team_inventory_summary(team_id: str):
    return await crud.get_team_inventory_summary(team_id)