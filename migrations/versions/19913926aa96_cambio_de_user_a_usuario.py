"""Cambio de User a Usuario

Revision ID: 19913926aa96
Revises: 187d8b6c2998
Create Date: 2025-05-01 01:57:42.750319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19913926aa96'
down_revision = '187d8b6c2998'
branch_labels = None
depends_on = None


def upgrade():
    # Crear nuevas tablas
    op.create_table('personaje',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=250), nullable=False),
        sa.Column('altura', sa.String(length=250), nullable=False),
        sa.Column('peso', sa.String(length=250), nullable=False),
        sa.Column('genero', sa.String(length=250), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )
    op.create_table('planeta',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=250), nullable=False),
        sa.Column('clima', sa.String(length=250), nullable=False),
        sa.Column('terreno', sa.String(length=250), nullable=False),
        sa.Column('poblacion', sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )
    op.create_table('usuario',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password', sa.String(length=128), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('fecha_de_subscripcion', sa.DateTime(), nullable=False),
        sa.Column('nombre', sa.String(length=120), nullable=False),
        sa.Column('apellido', sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_table('favorito_personaje',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('personaje_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['personaje_id'], ['personaje.id'], ),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('usuario_id', 'personaje_id', name='unique_usuario_personaje')
    )
    op.create_table('favorito_planeta',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('planeta_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['planeta_id'], ['planeta.id'], ),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('usuario_id', 'planeta_id', name='unique_usuario_planeta')
    )
    
    # Eliminar las tablas antiguas con CASCADE
    op.execute('DROP TABLE IF EXISTS "user" CASCADE')
    op.execute('DROP TABLE IF EXISTS "planet" CASCADE')
    op.execute('DROP TABLE IF EXISTS "favorite_planet" CASCADE')
    op.execute('DROP TABLE IF EXISTS "favorite_character" CASCADE')
    op.execute('DROP TABLE IF EXISTS "character" CASCADE')


def downgrade():
    # Volver a crear las tablas originales si es necesario
    op.create_table('character',
        sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('character_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(length=250), nullable=False),
        sa.Column('height', sa.VARCHAR(length=250), nullable=False),
        sa.Column('mass', sa.VARCHAR(length=250), nullable=False),
        sa.Column('gender', sa.VARCHAR(length=250), nullable=False),
        sa.PrimaryKeyConstraint('id', name='character_pkey'),
        sa.UniqueConstraint('name', name='character_name_key')
    )
    op.create_table('favorite_character',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.Column('character_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['character_id'], ['character.id'], name='favorite_character_character_id_fkey'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite_character_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='favorite_character_pkey'),
        sa.UniqueConstraint('user_id', 'character_id', name='unique_user_character')
    )
    op.create_table('favorite_planet',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.Column('planet_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], name='favorite_planet_planet_id_fkey'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite_planet_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='favorite_planet_pkey'),
        sa.UniqueConstraint('user_id', 'planet_id', name='unique_user_planet')
    )
    op.create_table('planet',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('name', sa.VARCHAR(length=250), nullable=False),
        sa.Column('climate', sa.VARCHAR(length=250), nullable=False),
        sa.Column('terrain', sa.VARCHAR(length=250), nullable=False),
        sa.Column('population', sa.INTEGER(), nullable=False),
        sa.PrimaryKeyConstraint('id', name='planet_pkey'),
        sa.UniqueConstraint('name', name='planet_name_key')
    )
    op.create_table('user',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('email', sa.VARCHAR(length=120), nullable=False),
        sa.Column('password', sa.VARCHAR(length=128), nullable=False),
        sa.Column('is_active', sa.BOOLEAN(), nullable=False),
        sa.PrimaryKeyConstraint('id', name='user_pkey'),
        sa.UniqueConstraint('email', name='user_email_key')
    )

    # Eliminar las tablas nuevas
    op.drop_table('favorito_planeta')
    op.drop_table('favorito_personaje')
    op.drop_table('usuario')
    op.drop_table('planeta')
    op.drop_table('personaje')

