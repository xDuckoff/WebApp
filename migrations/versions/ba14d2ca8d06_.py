"""empty message

Revision ID: ba14d2ca8d06
Revises: b14c941737a5
Create Date: 2017-08-16 18:28:41.509775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba14d2ca8d06'
down_revision = 'b14c941737a5'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('feedback', 'text')
    op.add_column('feedback', sa.Column('text', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('feedback', 'text')
    op.add_column('feedback', sa.Column('text', sa.String(length=256), nullable=True))
