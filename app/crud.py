from typing import List, Optional
from sqlalchemy import and_, or_
from .database import database
from .models import public_components, team_components

# === PUBLIC COMPONENTS ===

async def create_public_component(component_data: dict):
    query = public_components.insert().values(**component_data)
    return await database.execute(query)

async def get_public_component(component_id: str):
    query = public_components.select().where(public_components.c.id == component_id)
    return await database.fetch_one(query)

async def get_all_public_components():
    query = public_components.select()
    return await database.fetch_all(query)

async def update_public_component(component_id: str, component_data: dict):
    # Only update fields that aren't None
    update_data = {k: v for k, v in component_data.items() if v is not None}
    if not update_data:
        return False
    
    query = public_components.update().where(public_components.c.id == component_id).values(**update_data)
    result = await database.execute(query)
    return result > 0

async def delete_public_component(component_id: str):
    query = public_components.delete().where(public_components.c.id == component_id)
    result = await database.execute(query)
    return result > 0

async def search_public_components(
    search_text: Optional[str] = None,
    category: Optional[str] = None,
    vendor: Optional[str] = None,
    max_cost: Optional[float] = None
):
    query = public_components.select()
    conditions = []
    
    if search_text:
        conditions.append(
            or_(
                public_components.c.name.ilike(f"%{search_text}%"),
                public_components.c.description.ilike(f"%{search_text}%")
            )
        )
    if category:
        conditions.append(public_components.c.category.ilike(f"%{category}%"))
    if vendor:
        conditions.append(public_components.c.vendor.ilike(f"%{vendor}%"))
    if max_cost:
        conditions.append(public_components.c.cost <= max_cost)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    return await database.fetch_all(query)

async def get_categories():
    query = public_components.select(public_components.c.category).distinct()
    result = await database.fetch_all(query)
    return [row.category for row in result]

async def get_vendors():
    query = public_components.select(public_components.c.vendor).distinct()
    result = await database.fetch_all(query)
    return [row.vendor for row in result]

# === TEAM COMPONENTS ===

async def create_team_component(component_data: dict):
    query = team_components.insert().values(**component_data)
    return await database.execute(query)

async def get_team_component(component_id: int):
    query = team_components.select().where(team_components.c.id == component_id)
    return await database.fetch_one(query)

async def get_team_components(team_id: str):
    query = team_components.select().where(team_components.c.team_id == team_id)
    return await database.fetch_all(query)

async def update_team_component(component_id: int, component_data: dict):
    # Only update fields that aren't None
    update_data = {k: v for k, v in component_data.items() if v is not None}
    if not update_data:
        return False
    
    query = team_components.update().where(
        team_components.c.id == component_id
    ).values(**update_data)
    result = await database.execute(query)
    return result > 0

async def delete_team_component(component_id: int):
    query = team_components.delete().where(team_components.c.id == component_id)
    result = await database.execute(query)
    return result > 0

async def update_component_quantity(component_id: int, new_quantity: int):
    query = team_components.update().where(
        team_components.c.id == component_id
    ).values(quantity=new_quantity)
    return await database.execute(query)

# === TEAM INVENTORY SUMMARY ===

async def get_team_inventory_summary(team_id: str):
    query = team_components.select().where(team_components.c.team_id == team_id)
    components = await database.fetch_all(query)
    
    total_items = sum(comp.quantity for comp in components)
    unique_components = len(components)
    
    return {
        "team_id": team_id,
        "total_items": total_items,
        "unique_components": unique_components
    }
