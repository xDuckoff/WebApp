"""empty message

Revision ID: a14df3755bdc
Revises: bf6d73bfd002
Create Date: 2017-06-18 11:02:27.648313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a14df3755bdc'
down_revision = 'bf6d73bfd002'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat', sa.Column('remove_time', sa.Integer(), nullable=True))
    op.add_column('message', sa.Column('message_remove_time', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'message_remove_time')
    op.drop_column('chat', 'remove_time')
    # ### end Alembic commands ###