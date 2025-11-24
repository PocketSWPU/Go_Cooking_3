from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Text, SmallInteger, text


# Association table for many-to-many relationship between dishes and ingredients
class DishIngredientLink(SQLModel, table=True):
    __tablename__ = "dish_ingredients"
    dish_id: int = Field(foreign_key="dish.id", primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredient.id", primary_key=True)
    usage: str = Field(default="", sa_column=Column("usage", Text, server_default=""))  # 用量
    create_time: Optional[datetime] = Field(
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )
    modify_time: Optional[datetime] = Field(
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    )

    # Relationships
    dish: Optional["Dish"] = Relationship(back_populates="dish_ingredients")
    ingredient: Optional["Ingredient"] = Relationship(back_populates="dish_ingredients")


class Dish(SQLModel, table=True):
    __tablename__ = "dish"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    dish_name: str = Field(default="", max_length=255, sa_column=Column("dish_name", String, server_default=""))
    difficult: int = Field(default=1, sa_column=Column("difficult", SmallInteger, server_default="1"))  # 1简单 2中等 3复杂
    create_time: Optional[datetime] = Field(
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )
    modify_time: Optional[datetime] = Field(
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    )

    # Relationships
    steps: List["DishStep"] = Relationship(back_populates="dish")
    # Link ingredients with usage information
    ingredients: List["Ingredient"] = Relationship(
        back_populates="dishes",
        link_model=DishIngredientLink
    )
    dish_ingredients: List[DishIngredientLink] = Relationship(back_populates="dish")


class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredient"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    ingredient_name: str = Field(default="", max_length=255, sa_column=Column("ingredient_name", String, server_default=""))
    type: int = Field(default=1, sa_column=Column("type", SmallInteger, server_default="1"))  # 1主料 2辅料 3调料
    create_time: Optional[datetime] = Field(
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )
    modify_time: Optional[datetime] = Field(
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    )

    # Relationship
    dishes: List["Dish"] = Relationship(
        back_populates="ingredients",
        link_model=DishIngredientLink
    )
    dish_ingredients: List["DishIngredientLink"] = Relationship(back_populates="ingredient")


class DishStep(SQLModel, table=True):
    __tablename__ = "dish_step"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    dish_id: int = Field(foreign_key="dish.id")
    step_order: int = Field(default=0, sa_column=Column("step_order", SmallInteger, server_default="0"))
    step_text: str = Field(default="", sa_column=Column("step_text", Text, server_default=""))
    create_time: Optional[datetime] = Field(
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )
    modify_time: Optional[datetime] = Field(
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    )

    # Relationship
    dish: Optional[Dish] = Relationship(back_populates="steps")


