"""not nullable dataset_id in device

Revision ID: b102a73cb332
Revises: 84ad85d59d33
Create Date: 2024-09-29 00:58:56.200881

"""
from alembic import op
import sqlalchemy as sa
import flask_security


# revision identifiers, used by Alembic.
revision = 'b102a73cb332'
down_revision = '84ad85d59d33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('device', schema=None) as batch_op:
        batch_op.alter_column('key',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
        batch_op.alter_column('dataset_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('device', schema=None) as batch_op:
        batch_op.alter_column('dataset_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('key',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)

    # ### end Alembic commands ###
