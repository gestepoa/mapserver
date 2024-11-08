"""update table map_points comments

Revision ID: 6fbbd2546919
Revises: 18f8e43a0cc1
Create Date: 2024-11-06 00:58:31.905730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fbbd2546919'
down_revision: Union[str, None] = '18f8e43a0cc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('map_points', sa.Column('spot_short_name', sa.String(length=255), nullable=False, comment='点位简称'))
    op.add_column('map_points', sa.Column('spot_name_EN', sa.String(length=255), nullable=False, comment='点位英文名称'))
    op.add_column('map_points', sa.Column('spot_short_name_EN', sa.String(length=255), nullable=False, comment='点位英文简称'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('map_points', 'spot_short_name_EN')
    op.drop_column('map_points', 'spot_name_EN')
    op.drop_column('map_points', 'spot_short_name')
    # ### end Alembic commands ###