"""Create users table

Revision ID: 6fa62ec62bfd
Revises: bf4e20f0ac81
Create Date: 2021-11-25 19:52:29.468041

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = '6fa62ec62bfd'
down_revision = 'bf4e20f0ac81'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
    sa.Column('email', sa.String(50), nullable=False, unique=True),
    sa.Column('password', sa.String(250), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()'))
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
