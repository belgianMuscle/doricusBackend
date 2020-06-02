"""empty message

Revision ID: 8a3db4581eac
Revises: 99c86b9e456a
Create Date: 2020-06-02 10:53:21.241115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a3db4581eac'
down_revision = '99c86b9e456a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Member', sa.Column('email', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Member', 'email')
    # ### end Alembic commands ###