"""empty message

Revision ID: 9ba31c8e5ee5
Revises: c4f6fee3d0e5
Create Date: 2017-08-12 16:42:44.655176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ba31c8e5ee5'
down_revision = 'c4f6fee3d0e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chat', 'create_time')
    op.drop_column('chat', 'remove_time')
    op.add_column('chat', sa.Column('create_time', sa.DateTime(), nullable=False))
    op.add_column('chat', sa.Column('remove_time', sa.DateTime(), nullable=True))
    op.add_column('code', sa.Column('create_time', sa.DateTime(), nullable=False))
    op.add_column('code', sa.Column('remove_time', sa.DateTime(), nullable=True))
    op.drop_column('code', 'code_remove_time')
    op.drop_column('code', 'code_create_time')
    op.add_column('message', sa.Column('create_time', sa.DateTime(), nullable=False))
    op.add_column('message', sa.Column('remove_time', sa.DateTime(), nullable=True))
    op.drop_column('message', 'message_create_time')
    op.drop_column('message', 'message_remove_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('message_remove_time', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('message', sa.Column('message_create_time', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('message', 'remove_time')
    op.drop_column('message', 'create_time')
    op.add_column('code', sa.Column('code_create_time', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('code', sa.Column('code_remove_time', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('code', 'remove_time')
    op.drop_column('code', 'create_time')
    op.drop_column('chat', 'remove_time')
    op.drop_column('chat', 'create_time')
    op.add_column('chat', sa.Column('create_time', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('chat', sa.Column('remove_time', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
