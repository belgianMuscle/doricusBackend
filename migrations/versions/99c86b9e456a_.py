"""empty message

Revision ID: 99c86b9e456a
Revises: 80f0f29d2461
Create Date: 2020-06-01 23:50:18.032280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99c86b9e456a'
down_revision = '80f0f29d2461'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Member', sa.Column('full_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Member', 'full_name')
    # ### end Alembic commands ###
