# exercises/security-basics/app/routers/items.py
# L10 — Secure item endpoints

import re
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field, field_validator
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
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
        # Remove HTML tags and trim surrounding whitespace
        value = re.sub(r"<[^>]*>", "", value).strip()
        return value

    @field_validator("name")
    @classmethod
    def validate_name_not_blank(cls, value: str) -> str:
        if not value:
            raise ValueError("Name cannot be blank")
        return value


# TODO: Implement GET /items — list items
# Include a comment about SQL injection prevention
@router.get("/")
@limiter.limit("60/minute")
def list_items(request: Request):
    return {"items": []}
    """
    Returns all items.

    Security note: SQL injection prevention
    --------------------------------------
    Vulnerable (NEVER do this):
        query = f"SELECT * FROM items WHERE name = '{user_input}'"

    Safe (parameterized query):
        db.execute(select(Item).where(Item.name == user_input))

    Explain WHY parameterized queries prevent SQL injection.
    
    Parameterized queries keep SQL code separate from user-provided data
    #its better to never build SQL by putting user input directly into the SQL string. one should use parameters so the database knows

    """
    #pass  # TODO: return sample items list
    return {"items": []}


# TODO: Implement POST /items — create an item using ItemCreate schema
# The sanitizer on the schema handles input cleaning automatically
@router.post("/")
@limiter.limit("20/minute")
def create_item(request: Request, item: ItemCreate):
    """Creates an item after input validation and sanitization."""
    return {
        "message": "item created successfully",
        "item": item.model_dump()
    }
    
    