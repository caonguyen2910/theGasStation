"""Tạo bảng flights và passengers

Revision ID: 0576a157baa0
Revises:
Create Date: 2023-02-28 13:57:18.010414

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision = '0576a157baa0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cayxangpoint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('time', sa.String(), nullable=False),
    sa.Column('img', sa.String(), nullable=False),
    sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POINT', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # op.create_index('idx_cayxangpoint_geom', 'cayxangpoint', ['geom'], unique=False, postgresql_using='gist', postgresql_ops={})
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_index('idx_cayxangpoint_geom', table_name='cayxangpoint', postgresql_using='gist', postgresql_ops={})
    op.drop_table('cayxangpoint')
    # ### end Alembic commands ###
