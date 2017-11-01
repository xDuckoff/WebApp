"""empty message

Revision ID: 9e01f73568c2
Revises: 0bd36fc92dfa
Create Date: 2017-11-01 21:14:11.734062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e01f73568c2'
down_revision = '0bd36fc92dfa'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('feedback', 'trello_link', type_=sa.Text())


def downgrade():
    op.alter_column('feedback', 'trello_link', type_=sa.String(length=256))
