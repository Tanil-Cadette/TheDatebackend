"""add  models

Revision ID: a17893bb2b40
Revises: 74e1d13ce89e
Create Date: 2023-01-31 17:27:13.223821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a17893bb2b40'
down_revision = '74e1d13ce89e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('date', schema=None) as batch_op:
        batch_op.alter_column('friend_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('date', schema=None) as batch_op:
        batch_op.alter_column('friend_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###