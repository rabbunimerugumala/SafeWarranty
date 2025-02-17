"""Fix backref conflict

Revision ID: eb1eaa31479a
Revises: 4f33fa9db4a6
Create Date: 2025-01-14 18:18:10.445484

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'eb1eaa31479a'
down_revision = '4f33fa9db4a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('warranty_card', schema=None) as batch_op:
        batch_op.alter_column('user_id',
                              existing_type=sa.INTEGER(),
                              nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('warranty_card', schema=None) as batch_op:
        batch_op.alter_column('user_id',
                              existing_type=sa.INTEGER(),
                              nullable=False)

    # ### end Alembic commands ###
