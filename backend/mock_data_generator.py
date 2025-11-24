"""
Mock data generator for GoCooking 3
This module provides utilities to generate mock data for testing purposes
"""
import random
import sys
import os
from datetime import datetime

# Add the project root to the Python path so imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import get_db, create_db_and_tables
from backend.crud import add_dish_with_ingredients_and_steps
from backend import schemas

# Sample data for generating mock entries
dish_names = [
    "宫保鸡丁", "麻婆豆腐", "红烧肉", "糖醋排骨", "鱼香肉丝",
    "青椒肉丝", "西红柿鸡蛋", "回锅肉", "水煮鱼", "酸辣土豆丝",
    "蒜蓉西兰花", "红烧茄子", "干煸豆角", "白切鸡", "清蒸鲈鱼"
]

main_ingredients = [
    "鸡肉", "豆腐", "猪肉", "排骨", "鸡蛋", "土豆", "鲈鱼", "牛肉", "虾仁", "羊肉",
    "鸭肉", "三文鱼", "白菜", "萝卜", "茄子", "豆皮", "粉丝", "面条", "米饭", "玉米"
]

secondary_ingredients = [
    "胡萝卜", "青椒", "洋葱", "蒜苔", "豆芽", "韭菜", "芹菜", "香菜", "大葱", "生姜",
    "大蒜", "小米椒", "青蒜", "红椒", "金针菇", "香菇", "木耳", "紫菜", "海带", "冬瓜"
]

seasonings = [
    "料酒", "生抽", "老抽", "醋", "糖", "盐", "胡椒粉", "淀粉", "豆瓣酱", "花椒",
    "八角", "桂皮", "香叶", "耗油", "香油", "郫县豆瓣酱", "豆瓣酱", "甜面酱", "番茄酱", "辣椒油"
]

step_descriptions = [
    "将食材清洗干净，切成适当大小的块/片/丝",
    "热锅下油，放入葱姜蒜爆香",
    "下入主料翻炒至变色",
    "加入调料翻炒均匀",
    "加入适量清水或高汤，盖锅焖煮",
    "大火收汁，勾芡，出锅装盘",
    "将腌制好的食材下锅炒制",
    "炒制过程中注意火候，防止糊锅",
    "汤汁快收干时加入配菜",
    "起锅前撒上葱花或香菜点缀"
]

def generate_mock_dish():
    """
    Generate a complete mock dish with ingredients and steps
    Returns a dictionary containing dish data, ingredients, and steps
    """
    dish_name = random.choice(dish_names)
    difficult = random.choice([1, 2, 3])  # 1简单 2中等 3复杂

    # Generate random number of ingredients (3-8)
    num_ingredients = random.randint(3, 8)
    ingredients = []

    for _ in range(num_ingredients):
        # Randomly choose between main ingredient, secondary ingredient, or seasoning
        ingredient_type = random.choice([1, 2, 3])  # 1主料 2辅料 3调料
        if ingredient_type == 1:
            ingredient_name = random.choice(main_ingredients)
        elif ingredient_type == 2:
            ingredient_name = random.choice(secondary_ingredients)
        else:  # ingredient_type == 3
            ingredient_name = random.choice(seasonings)

        # Generate random usage description
        usages = ["适量", "少许", "一大勺", "一小勺", "按口味添加", "200克", "300克", "1根", "2个", "半斤"]
        usage = random.choice(usages)

        ingredients.append({
            "ingredient_name": ingredient_name,
            "type": ingredient_type,
            "usage": usage
        })

    # Generate random number of steps (4-10)
    num_steps = random.randint(4, 10)
    steps = []
    for i in range(num_steps):
        step_text = random.choice(step_descriptions) + f" (步骤 {i+1})"
        steps.append({
            "step_order": i+1,
            "step_text": step_text
        })

    return {
        "dish_name": dish_name,
        "difficult": difficult,
        "ingredients": ingredients,
        "steps": steps
    }

def generate_and_insert_mock_dish():
    """
    Generate a mock dish with ingredients and steps, then insert into the database
    This function handles the database operations internally using the proper add function
    """
    # Create database tables first (in case this is the first run)
    try:
        create_db_and_tables()
    except Exception:
        # If database connection fails, that's OK for this test - we just want to show the mechanism
        pass

    # Generate mock data
    mock_data = generate_mock_dish()

    # Get database session
    db_gen = get_db()
    db = next(db_gen)

    try:
        # Create dish request object with all related data
        dish_request = schemas.DishAddRequest(
            dish_name=mock_data["dish_name"],
            difficult=mock_data["difficult"],
            ingredients=[
                schemas.DishIngredientCreate(
                    ingredient_name=ing["ingredient_name"],
                    type=ing["type"],
                    usage=ing["usage"]
                )
                for ing in mock_data["ingredients"]
            ],
            steps=[
                schemas.DishStepCreateForDish(
                    step_order=step["step_order"],
                    step_text=step["step_text"]
                )
                for step in mock_data["steps"]
            ]
        )

        # Use the proper function that handles dish-ingredient relationships
        created_dish = add_dish_with_ingredients_and_steps(db, dish_request)

        print(f"+ Created dish: {created_dish.dish_name} (ID: {created_dish.id})")
        print(f"+ Difficulty: {created_dish.difficult} ({'简单' if created_dish.difficult == 1 else '中等' if created_dish.difficult == 2 else '复杂'})")

        # Load full dish details to verify relationships
        from backend.crud import get_dish_with_details
        dish_detail = get_dish_with_details(db, created_dish.id)

        if dish_detail:
            print(f"+ Created with {len(dish_detail['ingredients'])} ingredients and {len(dish_detail['steps'])} steps")

        print(f"\n+ Successfully created mock dish with all related data:")
        print(f"  - Dish: {created_dish.dish_name}")
        print(f"  - Difficulty: {created_dish.difficult} ({'简单' if created_dish.difficult == 1 else '中等' if created_dish.difficult == 2 else '复杂'})")

        # Return the created data for verification
        result = {
            "dish": {
                "id": created_dish.id,
                "dish_name": created_dish.dish_name,
                "difficult": created_dish.difficult
            },
            "ingredients": [
                {
                    "ingredient_name": ing["ingredient_name"],
                    "type": ing["type"],
                    "usage": ing["usage"]
                } for ing in mock_data["ingredients"]
            ],
            "steps": [
                {
                    "step_order": step["step_order"],
                    "step_text": step["step_text"]
                } for step in mock_data["steps"]
            ]
        }

        return result

    except Exception as e:
        print(f"- Error creating mock dish: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        # Close the database session
        next(db_gen, None)  # This properly closes the generator


def generate_multiple_mock_dishes(count=5):
    """
    Generate and insert multiple mock dishes
    """
    print(f"Generating {count} mock dishes...")
    created_dishes = []

    for i in range(count):
        print(f"\n--- Creating dish {i+1}/{count} ---")
        result = generate_and_insert_mock_dish()
        if result:
            created_dishes.append(result)
        else:
            print(f"- Failed to create dish {i+1}")

    print(f"\n+ Successfully created {len(created_dishes)} out of {count} dishes")
    return created_dishes


if __name__ == "__main__":
    print("GoCooking 3 - Mock Data Generator")
    print("="*40)

    # Example usage - create a single dish
    print("\nCreating a single mock dish with related data...")
    result = generate_and_insert_mock_dish()

    if result:
        print("\n" + "="*40)
        print("SUCCESSFULLY CREATED MOCK DISH")
        print("="*40)
        print(f"Dish: {result['dish']['dish_name']}")
        print(f"Difficulty: {result['dish']['difficult']}")
        print(f"Number of ingredients: {len(result['ingredients'])}")
        print(f"Number of steps: {len(result['steps'])}")

        print("\nIngredients:")
        for i, ing in enumerate(result['ingredients'], 1):
            ingredient_type = {1: '主料', 2: '辅料', 3: '调料'}[ing['type']]
            print(f"  {i}. {ing['ingredient_name']} (类型: {ingredient_type}, 用量: {ing['usage']})")

        print("\nSteps:")
        for step in result['steps']:
            print(f"  Step {step['step_order']}: {step['step_text']}")