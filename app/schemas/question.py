from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=12)
    category_id: int


class QuestionResponse(BaseModel):
    id: int
    text: str
    category: CategoryBase

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True