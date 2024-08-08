"""empty message

Revision ID: 02bf84b33c07
Revises: 13934a1ca6b4
Create Date: 2024-08-08 12:41:31.554970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02bf84b33c07'
down_revision = '13934a1ca6b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('short_desc', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('short_desc')

    # ### end Alembic commands ###