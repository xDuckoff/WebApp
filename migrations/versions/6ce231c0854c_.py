"""empty message

Revision ID: 6ce231c0854c
Revises: 23d6703cbe93
Create Date: 2017-03-07 15:33:04.539457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ce231c0854c'
down_revision = '23d6703cbe93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('author', sa.String(length=256), nullable=True),
    sa.Column('chat', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('code')
    # ### end Alembic commands ###
