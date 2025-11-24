"""Add usage column to dish_ingredients table

Revision ID: 001_add_usage_to_dish_ingredients
Revises: 
Create Date: 2023-11-22 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_add_usage_to_dish_ingredients'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add usage column to dish_ingredients table
    op.add_column('dish_ingredients', sa.Column('usage', sa.Text(), server_default="", nullable=False))
    
    # Add timestamps to dish_ingredients table
    op.add_column('dish_ingredients', sa.Column('create_time', sa.DateTime(), 
        server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('dish_ingredients', sa.Column('modify_time', sa.DateTime(), 
        server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True))


def downgrade():
    # Remove usage column from dish_ingredients table
    op.drop_column('dish_ingredients', 'usage')
    op.drop_column('dish_ingredients', 'create_time')
    op.drop_column('dish_ingredients', 'modify_time')