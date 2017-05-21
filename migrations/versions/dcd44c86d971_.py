"""empty message

Revision ID: dcd44c86d971
Revises: e0d83520f2ba
Create Date: 2017-05-21 15:03:45.715352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcd44c86d971'
down_revision = 'e0d83520f2ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('content_en', sa.Text(), nullable=True))
    op.add_column('message', sa.Column('content_ru', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'content_ru')
    op.drop_column('message', 'content_en')
    # ### end Alembic commands ###
