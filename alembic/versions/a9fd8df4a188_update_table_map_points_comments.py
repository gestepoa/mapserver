"""update table map_points comments

Revision ID: a9fd8df4a188
Revises: 6fbbd2546919
Create Date: 2024-11-07 23:18:14.674404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a9fd8df4a188'
down_revision: Union[str, None] = '6fbbd2546919'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('map_points', sa.Column('country_capital', sa.String(length=255), nullable=True, comment='所属国首都'))
    op.add_column('map_points', sa.Column('continental', sa.String(length=255), nullable=True, comment='所属大洲'))
    op.add_column('map_points', sa.Column('district', sa.String(length=255), nullable=True, comment='所属地区'))
    op.alter_column('map_points', 'spot_short_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True,
               existing_comment='点位简称')
    op.alter_column('map_points', 'spot_name_EN',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True,
               existing_comment='点位英文名称')
    op.alter_column('map_points', 'spot_short_name_EN',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True,
               existing_comment='点位英文简称')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('map_points', 'spot_short_name_EN',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False,
               existing_comment='点位英文简称')
    op.alter_column('map_points', 'spot_name_EN',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False,
               existing_comment='点位英文名称')
    op.alter_column('map_points', 'spot_short_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False,
               existing_comment='点位简称')
    op.drop_column('map_points', 'district')
    op.drop_column('map_points', 'continental')
    op.drop_column('map_points', 'country_capital')
    # ### end Alembic commands ###