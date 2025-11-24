from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import using absolute paths
from backend import crud, schemas
from backend.models import Ingredient
from backend.database import get_db

router = APIRouter(prefix="/cooking/ver3/ingredient", tags=["ingredient"])


@router.get("/list", response_model=schemas.APIResponse)
def get_all_ingredients(db: Session = Depends(get_db)):
    """
    获取所有配料列表
    """
    try:
        ingredients = crud.get_ingredients(db, skip=0, limit=1000)  # 获取所有配料
        return schemas.APIResponse(code=0, data=ingredients)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting ingredients: {str(e)}")


@router.post("/", response_model=schemas.APIResponse)
def create_ingredient(ingredient: schemas.IngredientCreate, db: Session = Depends(get_db)):
    """
    创建新配料
    """
    try:
        db_ingredient = crud.create_ingredient(db, ingredient)
        return schemas.APIResponse(code=0, data=db_ingredient)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating ingredient: {str(e)}")


@router.get("/{id}", response_model=schemas.APIResponse)
def get_ingredient(id: int, db: Session = Depends(get_db)):
    """
    根据ID获取配料详情
    """
    try:
        db_ingredient = crud.get_ingredient(db, id)
        if not db_ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return schemas.APIResponse(code=0, data=db_ingredient)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting ingredient: {str(e)}")
