from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import using absolute paths
from backend import crud, schemas
from backend.models import Dish
from backend.database import get_db

router = APIRouter(prefix="/cooking/ver3/dish", tags=["dish"])


@router.post("/select", response_model=schemas.APIResponse)
def select_dishes(query: schemas.DishQuery, db: Session = Depends(get_db)):
    from sqlalchemy.orm import selectinload
    from sqlmodel import select
    from backend.models import DishIngredientLink

    skip = query.page * query.size
    # Query dishes with ingredients using relationships
    statement = select(Dish).options(
        selectinload(Dish.dish_ingredients).selectinload(DishIngredientLink.ingredient)
    )
    if query.dish_name:
        statement = statement.where(Dish.dish_name.contains(query.dish_name))
    if query.difficult is not None:
        statement = statement.where(Dish.difficult == query.difficult)
    statement = statement.offset(skip).limit(query.size)
    result = db.execute(statement)
    dishes = result.scalars().all()

    total = crud.get_dish_count(db, dish_name=query.dish_name, difficult=query.difficult)

    # Create response data with basic dish info and main ingredients
    dish_cards = []
    for dish in dishes:
        # Extract main ingredients (type == 1)
        main_ingredients = []
        for dish_ing in dish.dish_ingredients:
            if dish_ing.ingredient.type == 1:  # 主料
                main_ingredients.append(dish_ing.ingredient.ingredient_name)

        # Limit to first 3 main ingredients for display
        main_ingredients_display = main_ingredients[:3]

        dish_cards.append({
            "id": dish.id,
            "dish_name": dish.dish_name,
            "difficult": dish.difficult,
            "main_ingredients": main_ingredients_display
        })

    # Return paginated result with total count
    return schemas.APIResponse(code=0, data={
        "items": dish_cards,
        "total": total,
        "page": query.page,
        "size": query.size
    })


@router.get("/detail/{id}", response_model=schemas.APIResponse)
def get_dish_detail(id: int, db: Session = Depends(get_db)):
    dish_detail = crud.get_dish_with_details(db, id)
    if not dish_detail:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    return schemas.APIResponse(code=0, data=dish_detail)


# Additional routes for CRUD operations
@router.post("/", response_model=schemas.APIResponse)
def create_dish(dish: schemas.DishCreate, db: Session = Depends(get_db)):
    db_dish = crud.create_dish(db, dish)
    return schemas.APIResponse(code=0, data=db_dish)


@router.get("/{id}", response_model=schemas.APIResponse)
def get_dish(id: int, db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, id)
    if not db_dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    return schemas.APIResponse(code=0, data=db_dish)


@router.put("/{id}", response_model=schemas.APIResponse)
def update_dish(id: int, dish: schemas.DishUpdate, db: Session = Depends(get_db)):
    db_dish = crud.update_dish(db, id, dish)
    if not db_dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    return schemas.APIResponse(code=0, data=db_dish)


@router.delete("/{id}", response_model=schemas.APIResponse)
def delete_dish(id: int, db: Session = Depends(get_db)):
    success = crud.delete_dish(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Dish not found")

    return schemas.APIResponse(code=0, message="Dish deleted successfully")


@router.post("/add/raw", response_model=schemas.APIResponse)
def add_dish_with_ingredients_and_steps(request: schemas.DishAddRequest, db: Session = Depends(get_db)):
    """
    菜品新增接口
    This endpoint receives a new dish with its main ingredients, auxiliary ingredients, and seasonings,
    writes ingredients to the ingredient table (checking for duplicates by name),
    creates mapping relationships between dishes and ingredients,
    and adds cooking steps with step order.
    """
    try:
        # Call the CRUD function to add the dish with ingredients and steps
        db_dish = crud.add_dish_with_ingredients_and_steps(db, request)

        return schemas.APIResponse(code=0, data={
            "id": db_dish.id,
            "dish_name": db_dish.dish_name,
            "difficult": db_dish.difficult,
            "message": "Dish added successfully"
        })
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding dish: {str(e)}")


@router.post("/history/create", response_model=schemas.APIResponse)
def create_dish_history(history: schemas.DishHistoryCreate, db: Session = Depends(get_db)):
    """
    Create a new dish history record
    """
    try:
        db_history = crud.create_dish_history(db, history)
        return schemas.APIResponse(code=0, data=db_history)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating dish history: {str(e)}")


@router.get("/{id}/history", response_model=schemas.APIResponse)
def get_dish_history(id: int, db: Session = Depends(get_db)):
    """
    Get dish cooking history by dish ID
    """
    try:
        history_list = crud.get_dish_history_by_dish_id(db, id)
        return schemas.APIResponse(code=0, data=history_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting dish history: {str(e)}")


@router.get("/{id}/cooking-count", response_model=schemas.APIResponse)
def get_cooking_count(id: int, db: Session = Depends(get_db)):
    """
    Get cooking count by dish ID
    """
    try:
        count = crud.get_cooking_count_by_dish_id(db, id)
        return schemas.APIResponse(code=0, data=count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting cooking count: {str(e)}")