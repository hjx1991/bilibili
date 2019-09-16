"""empty message

Revision ID: 94704d7df7bd
Revises: 5a3b9df44183
Create Date: 2019-09-16 18:54:27.748089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94704d7df7bd'
down_revision = '5a3b9df44183'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('img',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('img', sa.BLOB(), nullable=False),
    sa.Column('img_time', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('img')
    # ### end Alembic commands ###
