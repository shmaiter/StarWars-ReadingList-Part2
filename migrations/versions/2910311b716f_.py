"""empty message

Revision ID: 2910311b716f
Revises: cc9dd85de897
Create Date: 2021-04-07 03:04:16.050517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2910311b716f'
down_revision = 'cc9dd85de897'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('birthYear', sa.String(length=25), nullable=True),
    sa.Column('gender', sa.String(length=25), nullable=True),
    sa.Column('description', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('character')
    # ### end Alembic commands ###