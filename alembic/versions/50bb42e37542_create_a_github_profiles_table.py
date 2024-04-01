"""create a github profiles table

Revision ID: 50bb42e37542
Revises: e5aba0c892f7
Create Date: 2024-04-01 15:21:58.499631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50bb42e37542'
down_revision: Union[str, None] = 'e5aba0c892f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('github_profiles_user_id_fkey', 'github_profiles', type_='foreignkey')
    op.drop_column('github_profiles', 'user_id')
    op.add_column('posts', sa.Column('github_profile_id', sa.Integer(), nullable=True))
    op.drop_constraint('posts_user_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'github_profiles', ['github_profile_id'], ['id'])
    op.drop_column('posts', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_user_id_fkey', 'posts', 'users', ['user_id'], ['id'])
    op.drop_column('posts', 'github_profile_id')
    op.add_column('github_profiles', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('github_profiles_user_id_fkey', 'github_profiles', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
