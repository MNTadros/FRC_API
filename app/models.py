from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.database import metadata

public_components = Table(
    "public_components",
    metadata,
    Column("id", String, primary_key=True),                                                           # unique ID (part number / SKU)
    Column("name", String, nullable=False),                                                           # name of the part (must be provided)
    Column("vendor", String, nullable=False),                                                         # who makes/sells the part
    Column("category", String, nullable=False),                                                       # what type of part (electronics, mechanical, etc.)
    Column("cost", Float, nullable=False),                                                            # price of the part
    Column("source", String),                                                                         # optional URL / item link
    Column("description", Text),                                                                      # optional description
    Column("image_url", String),                                                                      # optional image URL
    Column("cad_file_url", String),                                                                   # optional CAD file URL
    Column("availability", String),                                                                   # availability status (In Stock, Out of Stock, etc.)
)

team_components = Table(
    "team_components",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),                                      # unique DB id
    Column("team_id", String, nullable=False),                                                        # which team owns this part
    Column("public_component_id", String, ForeignKey("public_components.id"), nullable=True),         # optional link to a public component (so you can inherit vendor, name, etc.)
    Column("name", String, nullable=False),                                                           # name of the component (overrides public name if needed)
    Column("vendor", String, nullable=False),                                                         # vendor (can be copied or changed from public)
    Column("quantity", Integer, nullable=False),                                                      # how many the team has
    Column("location", String),                                                                       # where it's stored
    Column("notes", Text),                                                                            # anything the team wants to add
    Column("added_by", String),                                                                       # who added it
    Column("last_updated", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),  # automatically set current time when inserted or updated
    Column("image_url", String),                                                                      # optional team image URL
    Column("cad_file_url", String),                                                                   # optional team CAD file URL
)