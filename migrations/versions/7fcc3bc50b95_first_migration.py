"""First_Migration

Revision ID: 7fcc3bc50b95
Revises: 
Create Date: 2023-01-10 07:11:37.799537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fcc3bc50b95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cars',
    sa.Column('id', sa.String(length=30), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('make', sa.String(length=28), nullable=False),
    sa.Column('created_at', sa.String(length=60), nullable=False),
    sa.Column('updated_at', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=28), nullable=False),
    sa.Column('password', sa.String(length=28), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('cars')
    # ### end Alembic commands ###
