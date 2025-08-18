from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PublicComponentCreate(BaseModel):
    id: str                             # REQUIRED - Part number/SKU
    name: str                           # REQUIRED - Component name
    vendor: str                         # REQUIRED - Who makes it
    category: str                       # REQUIRED - Electronics, Motors, etc.
    cost: float                         # REQUIRED - Price
    source: Optional[str] = None        # OPTIONAL - URL/link
    description: Optional[str] = None   # OPTIONAL - Details
    image_url: Optional[str] = None     # OPTIONAL - Image URL
    cad_file_url: Optional[str] = None  # OPTIONAL - CAD file URL
    availability: Optional[str] = None  # OPTIONAL - Availability status

class PublicComponentUpdate(BaseModel):
    name: Optional[str] = None
    vendor: Optional[str] = None
    category: Optional[str] = None
    cost: Optional[float] = None
    source: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    cad_file_url: Optional[str] = None
    availability: Optional[str] = None

class TeamComponentCreate(BaseModel):
    team_id: str                              # REQUIRED - Which team
    public_component_id: Optional[str] = None # OPTIONAL - Link to public catalog
    name: str                                 # REQUIRED - Component name
    vendor: str                               # REQUIRED - Vendor
    quantity: int                             # REQUIRED - How many
    location: Optional[str] = None            # OPTIONAL - Where stored
    notes: Optional[str] = None               # OPTIONAL - Team notes
    added_by: Optional[str] = None            # OPTIONAL - Who added it
    image_url: Optional[str] = None           # OPTIONAL - Team image URL
    cad_file_url: Optional[str] = None        # OPTIONAL - Team CAD file URL

class TeamComponentUpdate(BaseModel):
    name: Optional[str] = None
    vendor: Optional[str] = None
    quantity: Optional[int] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    added_by: Optional[str] = None
    image_url: Optional[str] = None
    cad_file_url: Optional[str] = None

class TeamImageUpdate(BaseModel):
    image_url: str                            # REQUIRED - CDN image URL
    description: Optional[str] = None         # OPTIONAL - Image description

# === USER AUTHENTICATION SCHEMAS ===

class UserCreate(BaseModel):
    username: str                             # REQUIRED - Unique username
    email: str                                # REQUIRED - Unique email
    password: str                             # REQUIRED - Plain password (will be hashed)
    team_id: Optional[str] = None             # OPTIONAL - Team ID

class UserLogin(BaseModel):
    username: str                             # REQUIRED - Username for login
    password: str                             # REQUIRED - Password for login

class Token(BaseModel):
    access_token: str                         # JWT access token
    token_type: str                           # Token type (bearer)

class User(BaseModel):
    id: int                                   # User ID
    username: str                             # Username
    email: str                                # Email
    team_id: Optional[str] = None             # Team ID
    role: str                                 # User role
    is_active: bool                           # Account status
    created_at: datetime                      # Account creation date
