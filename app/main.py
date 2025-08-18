from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from contextlib import asynccontextmanager
from .database import database, metadata, engine
from . import crud
from .schemas import PublicComponentCreate, PublicComponentUpdate, TeamComponentCreate, TeamComponentUpdate, TeamImageUpdate

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

@app.get("/")
async def root():
    return {"message": "FRC Components API is running!"}

# === PUBLIC COMPONENTS ===

@app.post("/public-components/")
async def create_public_component(component: PublicComponentCreate):
    try:
        await crud.create_public_component(component.model_dump())
        return {"id": component.id, "message": "Component created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/public-components/")
async def get_public_components():
    components = await crud.get_all_public_components()
    return [dict(component) for component in components]

@app.get("/public-components/search")
async def search_public_components(
    q: Optional[str] = Query(None, description="Search in name, description, and ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    vendor: Optional[str] = Query(None, description="Filter by vendor"),
    max_cost: Optional[float] = Query(None, description="Maximum cost"),
    availability: Optional[str] = Query(None, description="Filter by availability status"),
    has_cad_files: Optional[bool] = Query(None, description="Filter components with CAD files"),
    has_images: Optional[bool] = Query(None, description="Filter components with images")
):
    components = await crud.search_public_components(
        q, category, vendor, max_cost, availability, has_cad_files, has_images
    )
    return [dict(component) for component in components]

@app.get("/public-components/{component_id}")
async def get_public_component(component_id: str):
    component = await crud.get_public_component(component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    return dict(component)

@app.put("/public-components/{component_id}")
async def update_public_component(component_id: str, component: PublicComponentUpdate):
    if not await crud.get_public_component(component_id):
        raise HTTPException(status_code=404, detail="Component not found")
    
    if not await crud.update_public_component(component_id, component.model_dump()):
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    return {"message": "Component updated successfully"}

@app.delete("/public-components/{component_id}")
async def delete_public_component(component_id: str):
    if not await crud.delete_public_component(component_id):
        raise HTTPException(status_code=404, detail="Component not found")
    return {"message": "Component deleted successfully"}

# === TEAM COMPONENTS ===

@app.post("/team-components/")
async def create_team_component(component: TeamComponentCreate):
    try:
        component_id = await crud.create_team_component(component.model_dump())
        return {"id": component_id, "message": "Team component created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/teams/{team_id}/components")
async def get_team_components(team_id: str):
    components = await crud.get_team_components(team_id)
    return [dict(component) for component in components]

@app.get("/team-components/{component_id}")
async def get_team_component(component_id: int):
    component = await crud.get_team_component(component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Team component not found")
    return dict(component)

@app.put("/team-components/{component_id}")
async def update_team_component(component_id: int, component: TeamComponentUpdate):
    if not await crud.get_team_component(component_id):
        raise HTTPException(status_code=404, detail="Team component not found")
    
    if not await crud.update_team_component(component_id, component.model_dump()):
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    return {"message": "Team component updated successfully"}

@app.delete("/team-components/{component_id}")
async def delete_team_component(component_id: int):
    if not await crud.delete_team_component(component_id):
        raise HTTPException(status_code=404, detail="Team component not found")
    return {"message": "Team component deleted successfully"}

@app.post("/teams/{team_id}/components/{component_id}/add-image")
async def add_image_to_team_component(team_id: str, component_id: int, image_data: TeamImageUpdate):
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

@app.post("/teams/{team_id}/add-image")
async def add_general_team_image(team_id: str, image_data: TeamImageUpdate):
    image_id = await crud.create_team_image(team_id, image_data.image_url, image_data.description)
    return {
        "message": "Team image URL added successfully",
        "team_id": team_id,
        "image_id": image_id,
        "image_url": image_data.image_url
    }

# === UTILITY ENDPOINTS ===

@app.get("/categories")
async def get_categories():
    return await crud.get_categories()

@app.get("/vendors")
async def get_vendors():
    return await crud.get_vendors()

@app.get("/availability-statuses")
async def get_availability_statuses():
    return await crud.get_availability_statuses()

@app.get("/components/with-cad-files")
async def get_components_with_cad_files():
    components = await crud.get_components_with_cad_files()
    return [dict(component) for component in components]

@app.get("/components/with-images")
async def get_components_with_images():
    components = await crud.get_components_with_images()
    return [dict(component) for component in components]

@app.get("/teams/{team_id}/components/with-cad-files")
async def get_team_components_with_cad_files(team_id: str):
    components = await crud.get_team_components_with_cad_files(team_id)
    return [dict(component) for component in components]

@app.get("/teams/{team_id}/components/with-images")
async def get_team_components_with_images(team_id: str):
    components = await crud.get_team_components_with_images(team_id)
    return [dict(component) for component in components]

@app.get("/teams/{team_id}/inventory/summary")
async def get_team_inventory_summary(team_id: str):
    return await crud.get_team_inventory_summary(team_id)