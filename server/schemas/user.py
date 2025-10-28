from pydantic import BaseModel, EmailStr, Field

# --- Base Schema ---
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

# --- Signup Schema ---
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

# --- Login Schema ---
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- Response Schema ---
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # ✅ replaces orm_mode in Pydantic v2
