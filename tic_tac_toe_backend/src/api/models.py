"""
SQLAlchemy models for Tic Tac Toe backend.
Defines GameSession, Move, and PlayerStats for session handling,
move tracking, and player statistics.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base
import enum


# Game status enumeration
class GameStatus(str, enum.Enum):
    in_progress = "in_progress"
    completed = "completed"
    draw = "draw"


class PlayerStats(Base):
    """Tracks statistics for each player."""
    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    games_played = Column(Integer, default=0, nullable=False)
    games_won = Column(Integer, default=0, nullable=False)
    games_lost = Column(Integer, default=0, nullable=False)
    games_drawn = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    games_as_x = relationship(
        "GameSession",
        back_populates="player_x",
        foreign_keys="GameSession.player_x_id",
    )
    games_as_o = relationship(
        "GameSession",
        back_populates="player_o",
        foreign_keys="GameSession.player_o_id",
    )


class GameSession(Base):
    """Represents a Tic Tac Toe game session."""
    __tablename__ = "game_session"
    id = Column(Integer, primary_key=True, index=True)
    player_x_id = Column(Integer, ForeignKey("player_stats.id"), nullable=False)
    player_o_id = Column(Integer, ForeignKey("player_stats.id"), nullable=False)
    current_turn = Column(String(1), nullable=False)  # 'X' or 'O'
    status = Column(Enum(GameStatus), default=GameStatus.in_progress, nullable=False)
    winner = Column(String(1), nullable=True)  # 'X', 'O', or None for draw
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    player_x = relationship(
        "PlayerStats",
        back_populates="games_as_x",
        foreign_keys=[player_x_id],
    )
    player_o = relationship(
        "PlayerStats",
        back_populates="games_as_o",
        foreign_keys=[player_o_id],
    )
    moves = relationship(
        "Move",
        back_populates="game_session",
        cascade="all, delete",
    )


class Move(Base):
    """Represents a move made in a Tic Tac Toe session."""
    __tablename__ = "move"
    id = Column(Integer, primary_key=True, index=True)
    game_session_id = Column(Integer, ForeignKey("game_session.id"), nullable=False)
    player = Column(String(1), nullable=False)  # 'X' or 'O'
    x = Column(Integer, nullable=False)  # 0-2 board position (row)
    y = Column(Integer, nullable=False)  # 0-2 board position (col)
    move_num = Column(Integer, nullable=False)  # Move sequence/order (1-based)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    game_session = relationship("GameSession", back_populates="moves")
