"""create posts table

Revision ID: bf4e20f0ac81
Revises: 
Create Date: 2021-11-25 19:32:47.885719

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text
from sqlalchemy import ForeignKey


# revision identifiers, used by Alembic.
revision = 'bf4e20f0ac81'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(100), nullable=False),
    sa.Column('content', sa.String(250), nullable=False),
    sa.Column('published', sa.Boolean(), server_default=text('True')),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
    # sa.Column('user_id', sa.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
