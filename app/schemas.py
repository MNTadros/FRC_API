from pydantic import BaseModel
from typing import Optional

class PublicComponentCreate(BaseModel):
    id: str                             # REQUIRED - Part number/SKU
    name: str                           # REQUIRED - Component name
    vendor: str                         # REQUIRED - Who makes it
    category: str                       # REQUIRED - Electronics, Motors, etc.
    cost: float                         # REQUIRED - Price
    source: Optional[str] = None        # OPTIONAL - URL/link
    description: Optional[str] = None   # OPTIONAL - Details

class PublicComponentUpdate(BaseModel):
    name: Optional[str] = None
    vendor: Optional[str] = None
    category: Optional[str] = None
    cost: Optional[float] = None
    source: Optional[str] = None
    description: Optional[str] = None

class TeamComponentCreate(BaseModel):
    team_id: str                              # REQUIRED - Which team
    public_component_id: Optional[str] = None # OPTIONAL - Link to public catalog
    name: str                                 # REQUIRED - Component name
    vendor: str                               # REQUIRED - Vendor
    quantity: int                             # REQUIRED - How many
    location: Optional[str] = None            # OPTIONAL - Where stored
    notes: Optional[str] = None               # OPTIONAL - Team notes
    added_by: Optional[str] = None            # OPTIONAL - Who added it

class TeamComponentUpdate(BaseModel):
    name: Optional[str] = None
    vendor: Optional[str] = None
    quantity: Optional[int] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    added_by: Optional[str] = None
