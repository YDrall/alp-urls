"""create url table

Revision ID: 91317fd2c32e
Revises: 
Create Date: 2023-04-05 14:41:28.299315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91317fd2c32e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'url',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('user_id', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime()))


def downgrade() -> None:
    op.drop_table('url')
