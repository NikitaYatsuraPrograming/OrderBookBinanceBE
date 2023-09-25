"""update binance table(change int on bigint)

Revision ID: cffbdabfd853
Revises: b3a87a0fe346
Create Date: 2023-09-24 21:48:22.055559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cffbdabfd853'
down_revision: Union[str, None] = 'b3a87a0fe346'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
