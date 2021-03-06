"""empty message

Revision ID: a4ae558db061
Revises: 
Create Date: 2021-02-16 13:55:34.573037

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a4ae558db061'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=True)
    op.alter_column('venue', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('venue', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=False)
    # ### end Alembic commands ###
