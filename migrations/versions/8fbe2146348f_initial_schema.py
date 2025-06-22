"""Initial schema

Revision ID: 8fbe2146348f
Revises: 
Create Date: 2025-05-27 01:21:52.561095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import datetime


# revision identifiers, used by Alembic.
revision: str = '8fbe2146348f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create 'user' table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pixelId', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create 'roll' table
    op.create_table(
        'roll',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True, default=datetime.datetime.utcnow),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('roll')
    op.drop_table('user')
