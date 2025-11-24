from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel


class DishBase(SQLModel):
    dish_name: str
    difficult: int  # 1简单 2中等 3复杂


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    pass


class Dish(DishBase):
    id: Optional[int] = None
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True


class IngredientBase(SQLModel):
    ingredient_name: str
    type: int  # 1主料 2辅料 3调料


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: Optional[int] = None
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True


class DishIngredientDetail(BaseModel):
    id: int
    ingredient_name: str
    type: int  # 1主料 2辅料 3调料
    usage: str  # 用量
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True


class DishStepBase(SQLModel):
    dish_id: int
    step_order: int
    step_text: str


class DishStepCreate(DishStepBase):
    pass


class DishStepCreateForDish(SQLModel):  # New schema for dish creation
    step_order: int
    step_text: str


class DishStepUpdate(DishStepBase):
    pass


class DishStep(DishStepBase):
    id: Optional[int] = None
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True


from pydantic import BaseModel, Field  # Add Field import if not already present

# Request schemas
class DishQuery(BaseModel):
    page: int = 0
    size: int = 10
    dish_name: Optional[str] = Field(default="", alias="dishName")  # alias for frontend "dishName"
    difficult: Optional[int] = None  # 1简单 2中等 3复杂, None means no filter

    class Config:
        # Allow both snake_case and camelCase field names
        allow_population_by_field_name = True


class DishIngredientCreate(SQLModel):
    ingredient_name: str
    type: int  # 1主料 2辅料 3调料
    usage: str  # 用量


class DishAddRequest(BaseModel):
    dish_name: str
    difficult: int  # 1简单 2中等 3复杂
    ingredients: List[DishIngredientCreate]
    steps: List[DishStepCreateForDish]


# Response schemas
class DishCard(BaseModel):
    id: int
    dish_name: str
    difficult: int
    tags: List[str]  # This could be derived from ingredients or other related data

    class Config:
        from_attributes = True


class DishDetail(BaseModel):
    id: int
    dish_name: str
    difficult: int
    ingredients: List[DishIngredientDetail]  # This will include usage info
    steps: List[DishStep]
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True


class DishHistoryBase(SQLModel):
    dish_id: int
    cooking_rating: int  # 1很棒 2还行 3一般 4拉胯


class DishHistoryCreate(DishHistoryBase):
    pass


class DishHistory(DishHistoryBase):
    id: Optional[int] = None
    cooking_time: datetime
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True


class APIResponse(BaseModel):
    code: int
    data: Optional[object] = None
    message: Optional[str] = None