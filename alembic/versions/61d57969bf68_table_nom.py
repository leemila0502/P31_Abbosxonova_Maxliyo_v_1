"""Table nom

Revision ID: 61d57969bf68
Revises: 
Create Date: 2025-06-02 12:51:35.096631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61d57969bf68'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.alter_column(
        'userss',                 # <-- Jadval nomi
        'name',              # <-- Eski ustun nomi
        new_column_name='fullname'  # <-- Yangi ustun nomi
    )

def downgrade():
    op.alter_column(
        'userss',
        'name',
        new_column_name='fullname'
    )