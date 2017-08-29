"""empty message

Revision ID: 0bd36fc92dfa
Revises: ba14d2ca8d06
Create Date: 2017-08-24 16:25:09.918562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bd36fc92dfa'
down_revision = 'ba14d2ca8d06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feedback', sa.Column('trello_link', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feedback', 'trello_link')
    # ### end Alembic commands ###