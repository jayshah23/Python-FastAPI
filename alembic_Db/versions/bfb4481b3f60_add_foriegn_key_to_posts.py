"""add foriegn key to posts

Revision ID: bfb4481b3f60
Revises: 6fa62ec62bfd
Create Date: 2021-11-25 20:09:11.889326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfb4481b3f60'
down_revision = '6fa62ec62bfd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=[
                          'user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
