"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2023-11-16 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, Text, ForeignKey
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create dish table
    op.create_table(
        'dish',
        Column('id', Integer, primary_key=True, index=True),
        Column('dish_name', String, server_default=""),
        Column('difficult', SmallInteger, server_default="1"),  # 1简单 2中等 3复杂
        Column('create_time', DateTime, server_default=func.current_timestamp()),
        Column('modify_time', DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    )

    # Create ingredient table
    op.create_table(
        'ingredient',
        Column('id', Integer, primary_key=True, index=True),
        Column('ingredient_name', String, server_default=""),
        Column('type', SmallInteger, server_default="1"),  # 1辅料 2配料
        Column('create_time', DateTime, server_default=func.current_timestamp()),
        Column('modify_time', DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    )

    # Create dish_step table
    op.create_table(
        'dish_step',
        Column('id', Integer, primary_key=True, index=True),
        Column('dish_id', Integer, ForeignKey('dish.id')),
        Column('step_order', Integer, server_default="0"),
        Column('step_text', Text, server_default=""),
        Column('create_time', DateTime, server_default=func.current_timestamp()),
        Column('modify_time', DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    )

    # Create association table for dish_ingredients
    op.create_table(
        'dish_ingredients',
        Column('dish_id', Integer, ForeignKey('dish.id'), primary_key=True),
        Column('ingredient_id', Integer, ForeignKey('ingredient.id'), primary_key=True)
    )


def downgrade() -> None:
    op.drop_table('dish_ingredients')
    op.drop_table('dish_step')
    op.drop_table('ingredient')
    op.drop_table('dish')