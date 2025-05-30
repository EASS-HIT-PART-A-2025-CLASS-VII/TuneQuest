"""add spotify_track_id to favorites and archived track

Revision ID: d51b7a44f7b6
Revises: dc5505d38900
Create Date: 2025-05-31 03:47:14.254722

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d51b7a44f7b6"
down_revision: Union[str, None] = "dc5505d38900"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop foreign key constraint and column referencing tracks first
    op.drop_constraint("favorites_track_id_fkey", "favorites", type_="foreignkey")
    op.drop_column("favorites", "track_id")

    # Now drop indexes and tracks table safely
    op.drop_index("ix_tracks_album", table_name="tracks")
    op.drop_index("ix_tracks_artist", table_name="tracks")
    op.drop_index("ix_tracks_id", table_name="tracks")
    op.drop_index("ix_tracks_title", table_name="tracks")
    op.drop_table("tracks")

    # Add new spotify_track_id column after that
    op.add_column(
        "favorites", sa.Column("spotify_track_id", sa.String(length=50), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "favorites",
        sa.Column("track_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.create_foreign_key(
        "favorites_track_id_fkey", "favorites", "tracks", ["track_id"], ["id"]
    )
    op.drop_column("favorites", "spotify_track_id")
    op.create_table(
        "tracks",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("artist", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("album", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("genre", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "rating",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name="tracks_pkey"),
    )
    op.create_index("ix_tracks_title", "tracks", ["title"], unique=False)
    op.create_index("ix_tracks_id", "tracks", ["id"], unique=False)
    op.create_index("ix_tracks_artist", "tracks", ["artist"], unique=False)
    op.create_index("ix_tracks_album", "tracks", ["album"], unique=False)
    # ### end Alembic commands ###
