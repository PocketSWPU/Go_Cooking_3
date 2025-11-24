from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from sqlmodel import select
from typing import Optional
import sys
import os

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import Dish, Ingredient, DishStep, DishIngredientLink, DishHistory
from backend import schemas


def get_dish(db: Session, dish_id: int):
    statement = select(Dish).where(Dish.id == dish_id)
    result = db.execute(statement)
    return result.scalar_one_or_none()


def get_dishes(db: Session, skip: int = 0, limit: int = 10, dish_name: str = "", difficult: Optional[int] = None):
    statement = select(Dish)
    if dish_name:
        # statement = statement.where(Dish.dish_name.contains(dish_name))
        statement = statement.where(Dish.dish_name.ilike(f"%{dish_name}%"))
    if difficult is not None:
        statement = statement.where(Dish.difficult == difficult)
    statement = statement.offset(skip).limit(limit)
    result = db.execute(statement)
    dishes = result.scalars().all()
    return dishes


def get_dish_count(db: Session, dish_name: str = "", difficult: Optional[int] = None):
    statement = select(func.count(Dish.id))
    if dish_name:
        statement = statement.where(Dish.dish_name.contains(dish_name))
    if difficult is not None:
        statement = statement.where(Dish.difficult == difficult)
    result = db.execute(statement)
    return result.scalar_one()


def create_dish(db: Session, dish: schemas.DishCreate):
    db_dish = Dish(dish_name=dish.dish_name, difficult=dish.difficult)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def update_dish(db: Session, dish_id: int, dish: schemas.DishUpdate):
    db_dish = get_dish(db, dish_id)
    if not db_dish:
        return None

    db_dish.dish_name = dish.dish_name
    db_dish.difficult = dish.difficult
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def delete_dish(db: Session, dish_id: int):
    db_dish = get_dish(db, dish_id)
    if not db_dish:
        return False

    db.delete(db_dish)
    db.commit()
    return True


def get_ingredient(db: Session, ingredient_id: int):
    statement = select(Ingredient).where(Ingredient.id == ingredient_id)
    result = db.execute(statement)
    return result.scalar_one_or_none()


def get_ingredients(db: Session, skip: int = 0, limit: int = 10):
    statement = select(Ingredient).offset(skip).limit(limit)
    result = db.execute(statement)
    return result.scalars().all()


def create_ingredient(db: Session, ingredient: schemas.IngredientCreate):
    db_ingredient = Ingredient(ingredient_name=ingredient.ingredient_name, type=ingredient.type)
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


def get_dish_step(db: Session, step_id: int):
    statement = select(DishStep).where(DishStep.id == step_id)
    result = db.execute(statement)
    return result.scalar_one_or_none()


def get_dish_steps(db: Session, dish_id: int):
    statement = select(DishStep).where(DishStep.dish_id == dish_id).order_by(DishStep.step_order)
    result = db.execute(statement)
    return result.scalars().all()


def create_dish_step(db: Session, step: schemas.DishStepCreate):
    db_step = DishStep(
        dish_id=step.dish_id,
        step_order=step.step_order,
        step_text=step.step_text
    )
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step


def get_dish_with_details(db: Session, dish_id: int):
    # Get dish with relationships preloaded
    dish = get_dish(db, dish_id)
    if not dish:
        return None

    # Load both ingredients and dish_ingredients relationships
    from sqlalchemy.orm import selectinload

    # Get dish with ingredients and dish_ingredients
    from sqlmodel import select
    statement = select(Dish).options(
        selectinload(Dish.ingredients),
        selectinload(Dish.dish_ingredients).selectinload(DishIngredientLink.ingredient)
    ).where(Dish.id == dish_id)

    result = db.execute(statement)
    dish = result.scalar_one_or_none()

    if not dish:
        return None

    # Combine ingredient info with usage info from dish_ingredients
    ingredients_with_usage = []
    for dish_ing in dish.dish_ingredients:
        ingredient = dish_ing.ingredient
        ingredients_with_usage.append({
            "id": ingredient.id,
            "ingredient_name": ingredient.ingredient_name,
            "type": ingredient.type,
            "usage": dish_ing.usage,
            "create_time": ingredient.create_time,
            "modify_time": ingredient.modify_time
        })

    # Sort ingredients by type
    sorted_ingredients = sorted(ingredients_with_usage, key=lambda x: x['type'])

    return {
        "id": dish.id,
        "dish_name": dish.dish_name,
        "difficult": dish.difficult,
        "ingredients": sorted_ingredients,
        "steps": dish.steps,
        "create_time": dish.create_time,
        "modify_time": dish.modify_time
    }


def add_dish_with_ingredients_and_steps(db: Session, dish_data: schemas.DishAddRequest):
    """
    Add a new dish with its ingredients and steps.
    This function creates the dish, checks for existing ingredients, creates new ones if needed,
    establishes relationships between dish and ingredients with usage, and adds the cooking steps.
    """
    # First, create the dish
    db_dish = Dish(dish_name=dish_data.dish_name, difficult=dish_data.difficult)
    db.add(db_dish)
    db.flush()  # This ensures the dish gets an ID without committing the transaction

    # Process ingredients
    for ingredient_data in dish_data.ingredients:
        # Check if ingredient already exists using SQLModel select
        statement = select(Ingredient).where(Ingredient.ingredient_name == ingredient_data.ingredient_name)
        result = db.execute(statement)
        existing_ingredient = result.scalar_one_or_none()

        if existing_ingredient:
            ingredient_id = existing_ingredient.id
        else:
            # Create new ingredient (without usage - usage is per dish)
            new_ingredient = Ingredient(
                ingredient_name=ingredient_data.ingredient_name,
                type=ingredient_data.type
            )
            db.add(new_ingredient)
            db.flush()  # Get the ID of the new ingredient
            ingredient_id = new_ingredient.id

        # Create the relationship between dish and ingredient with usage info
        dish_ingredient_link = DishIngredientLink(
            dish_id=db_dish.id,
            ingredient_id=ingredient_id,
            usage=ingredient_data.usage
        )
        db.add(dish_ingredient_link)

    # Process steps
    for step_data in dish_data.steps:
        # Create dish step, using the dish_id we just created
        step = DishStep(
            dish_id=db_dish.id,
            step_order=step_data.step_order,
            step_text=step_data.step_text
        )
        db.add(step)

    # Commit all changes
    db.commit()

    # Refresh to get the latest data
    db.refresh(db_dish)

    return db_dish


def create_dish_history(db: Session, dish_history: schemas.DishHistoryCreate):
    from datetime import datetime
    db_dish_history = DishHistory(
        dish_id=dish_history.dish_id,
        cooking_time=datetime.now(),
        cooking_rating=dish_history.cooking_rating
    )
    db.add(db_dish_history)
    db.commit()
    db.refresh(db_dish_history)
    return db_dish_history


def get_dish_history_by_dish_id(db: Session, dish_id: int):
    from sqlalchemy.orm import selectinload
    from sqlmodel import select
    statement = select(DishHistory).where(DishHistory.dish_id == dish_id).order_by(
        DishHistory.cooking_time.desc(),
        DishHistory.create_time.desc()
    )
    result = db.execute(statement)
    return result.scalars().all()


def get_cooking_count_by_dish_id(db: Session, dish_id: int):
    from sqlmodel import select, func
    statement = select(func.count(DishHistory.id)).where(DishHistory.dish_id == dish_id)
    result = db.execute(statement)
    return result.scalar_one()
