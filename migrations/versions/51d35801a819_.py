"""empty message

Revision ID: 51d35801a819
Revises: 9a8308b7223d
Create Date: 2017-04-26 23:06:23.068351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51d35801a819'
down_revision = '9a8308b7223d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('code', sa.Column('parent', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('code', 'parent')
    # ### end Alembic commands ###
