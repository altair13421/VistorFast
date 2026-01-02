"""initial Migration

Revision ID: e6bb45d2b79f
Revises: 
Create Date: 2026-01-01 15:01:51.930044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision: str = 'e6bb45d2b79f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    existing_tables = inspector.get_table_names()

    # Create tables with foreign keys defined inline
    if "artists" not in existing_tables:
        op.create_table(
            'artists',
            sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
            sa.Column('name', sa.String(), nullable=False, index=True),
            sa.Column('romaji_name', sa.String(), nullable=False, index=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
        )

    if 'genres' not in existing_tables:
        op.create_table(
            'genres',
            sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
            sa.Column('name', sa.String(), nullable=False, index=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
        )

    if 'albums' not in existing_tables:
        op.create_table(
            'albums',
            sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
            sa.Column('title', sa.String(), nullable=False, index=True),
            sa.Column('romaji_title', sa.String(), nullable=False, index=True),
            sa.Column('release_date', sa.DateTime(), nullable=True),
            sa.Column('album_art', sa.String(), nullable=True),
            sa.Column('artist_id', sa.Integer(), nullable=False, index=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
            sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
        )

    if 'songs' not in existing_tables:
        op.create_table(
            'songs',
            sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
            sa.Column('title', sa.String(), nullable=False, index=True),
            sa.Column('romaji_title', sa.String(), nullable=False, index=True),
            sa.Column('file_path', sa.String(), nullable=False, index=True),
            sa.Column('duration', sa.Integer(), nullable=False, index=True),
            sa.Column('track_number', sa.Integer(), nullable=False, index=True),
            sa.Column('times_played', sa.Integer(), nullable=False, default=0),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
            sa.Column('album_id', sa.Integer(), nullable=False, index=True),
            sa.ForeignKeyConstraint(['album_id'], ['albums.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
        )

    # Junction tables — FKs defined inline
    if 'song_artists' not in existing_tables:
        op.create_table(
            'song_artists',
            sa.Column('artist_id', sa.Integer(), nullable=False),
            sa.Column('song_id', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('artist_id', 'song_id'),
            sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['song_id'], ['songs.id'], ondelete='CASCADE'),
        )

    if 'song_genres' not in existing_tables:
        op.create_table(
            'song_genres',
            sa.Column('genre_id', sa.Integer(), nullable=False),
            sa.Column('song_id', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('genre_id', 'song_id'),
            sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['song_id'], ['songs.id'], ondelete='CASCADE'),
        )

    # Optional: Add indexes
    existing_indexes_songs = [idx['name'] for idx in inspector.get_indexes('songs')] if 'songs' in existing_tables else []
    if 'ix_songs_title' not in existing_indexes_songs and 'songs' in existing_tables:
        op.create_index('ix_songs_title', 'songs', ['title'])
    if 'ix_songs_romaji_title' not in existing_indexes_songs and 'songs' in existing_tables:
        op.create_index('ix_songs_romaji_title', 'songs', ['romaji_title'])
    if 'ix_songs_file_path' not in existing_indexes_songs and 'songs' in existing_tables:
        op.create_index('ix_songs_file_path', 'songs', ['file_path'])

    existing_indexes_albums = [idx['name'] for idx in inspector.get_indexes('albums')] if 'albums' in existing_tables else []
    if 'ix_albums_title' not in existing_indexes_albums and 'albums' in existing_tables:
        op.create_index('ix_albums_title', 'albums', ['title'])
    if 'ix_albums_romaji_title' not in existing_indexes_albums and 'albums' in existing_tables:
        op.create_index('ix_albums_romaji_title', 'albums', ['romaji_title'])

    if 'artists' in existing_tables:
        existing_indexes_artists = [idx['name'] for idx in inspector.get_indexes('artists')]
        if 'ix_artists_name' not in existing_indexes_artists:
            op.create_index('ix_artists_name', 'artists', ['name'])
        if 'ix_artists_romaji_name' not in existing_indexes_artists:
            op.create_index('ix_artists_romaji_name', 'artists', ['romaji_name'])


def downgrade():
    # Drop tables in reverse order — safe for SQLite
    op.drop_table('song_genres')
    op.drop_table('song_artists')
    op.drop_table('songs')
    op.drop_table('albums')
    op.drop_table('genres')
    op.drop_table('artists')
