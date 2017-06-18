"""empty message

Revision ID: f922f3febd0c
Revises: 91c22e93edd7
Create Date: 2017-06-18 08:33:35.580623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f922f3febd0c'
down_revision = '91c22e93edd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat', sa.Column('start_time', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chat', 'start_time')
    # ### end Alembic commands ###
