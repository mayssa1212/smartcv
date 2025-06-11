"""rename owner_id to user_id

Revision ID: 0f5b08123848
Revises: 9719c133a4ee
Create Date: 2023-10-15 14:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0f5b08123848'
down_revision: Union[str, None] = '9719c133a4ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. D'abord, supprimez la contrainte de clé étrangère si elle existe
    try:
        op.drop_constraint(op.f('cvs_owner_id_fkey'), 'cvs', type_='foreignkey')
    except Exception:
        pass  # La contrainte n'existe peut-être pas
    
    # 2. Ensuite, modifiez les contraintes de nullabilité sur owner_id
    op.alter_column('cvs', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    
    # 3. Maintenant, renommez la colonne
    op.alter_column('cvs', 'owner_id', new_column_name='user_id')
    
    # 4. Effectuez les autres modifications
    op.alter_column('cvs', 'data',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_column('cvs', 'created_at')
    op.alter_column('users', 'full_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('users', 'created_at')


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Ajout des colonnes supprimées
    op.add_column('users', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('cvs', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    
    # 2. Renommez la colonne
    op.alter_column('cvs', 'user_id', new_column_name='owner_id')
    
    # 3. Restaurez les contraintes de nullabilité
    op.alter_column('cvs', 'data',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('cvs', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('users', 'full_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    
    # 4. Recréez la contrainte de clé étrangère
    op.create_foreign_key(op.f('cvs_owner_id_fkey'), 'cvs', 'users', ['owner_id'], ['id'])



