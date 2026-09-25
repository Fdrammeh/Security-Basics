# exercises/security-basics/app/routers/items.py
# L10 — Secure item endpoints

import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

router = APIRouter()


# TODO: Define an ItemCreate schema with a "name" field (str, max 100)
# Add a @field_validator that sanitizes user input:
# - Strip leading/trailing whitespace
# - Remove HTML tags (use re.sub to strip <...> patterns)
# - Return the sanitized string
#
# Key concept: Input sanitization prevents stored XSS attacks.
# If user-submitted text is later displayed in a browser without escaping,
# any <script> tags would execute. Strip them before storing.
class ItemCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str = Field(default="", max_length=500)

    # TODO: Add @field_validator("name", "description") to sanitize
    @field_validator("name", "description") 
    @classmethod 
    def sanitize_input(cls, value: str) -> str:
        value = value.strip()

        return value


# TODO: Implement GET /items — list items
# Include a comment about SQL injection prevention
@router.get("/")
def list_items():
    """
    Returns all items.

    Security note: SQL injection prevention
    ----------------------------------------
    TODO: Add a comment here explaining VULNERABLE vs SAFE SQL patterns.

    Vulnerable (NEVER do this):
        query = f"SELECT * FROM items WHERE name = '{user_input}'"

    Safe (parameterized query):
        db.execute(select(Item).where(Item.name == user_input))

    Explain WHY parameterized queries prevent SQL injection.
    """
    #Parameterized queries keep SQL code separate from user-provided data
    #its better to never build SQL by putting user input directly into the SQL string. one should use parameters so the database knows
    #pass  # TODO: return sample items list


# TODO: Implement POST /items — create an item using ItemCreate schema
# The sanitizer on the schema handles input cleaning automatically
@router.post("/")
def create_item(item: ItemCreate):
    """
    Creates an item. Input is sanitized by the schema validator.

    TODO: Return the sanitized item data.
    """
    #pass  # TODO: implement
    return {
        "message": "item created successfully",
        "item": item
    }