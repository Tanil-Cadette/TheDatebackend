"""empty message

Revision ID: 21610bca3651
Revises: 
Create Date: 2023-02-08 22:42:38.235996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21610bca3651'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friend',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('interest', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('location_coords', sa.ARRAY(sa.String()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('date',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('place', sa.String(), nullable=True),
    sa.Column('location', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('date_completed', sa.Boolean(), nullable=True),
    sa.Column('friend_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['friend_id'], ['friend.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('date')
    op.drop_table('friend')
    # ### end Alembic commands ###
