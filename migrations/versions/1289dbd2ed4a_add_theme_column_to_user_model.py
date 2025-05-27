"""Add theme column to User model

Revision ID: 1289dbd2ed4a
Revises: 2a7bd95312dd
Create Date: 2024-05-26 16:55:23.123456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1289dbd2ed4a'
down_revision = '2a7bd95312dd'
branch_labels = None
depends_on = None


def upgrade():
    # Add theme column with a default value
    with op.batch_alter_table('user') as batch_op:
        batch_op.add_column(sa.Column('theme', sa.String(20), nullable=False, server_default='minimalist'))


def downgrade():
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_column('theme')
