from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from .connect import Base

# Auction Model
class Auction(Base):
    __tablename__ = "auctions"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    purse_amt = Column(Integer, nullable=False)
    min_bid = Column(Integer, nullable=True)
    bid_increase_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, onupdate=func.now(), default=func.now())


# Players Model
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    origin = Column(Enum("Overseas", "Native", name="player_origin"), nullable=False, default="Native")
    player_type = Column(Enum("Batsman", "Bowler","All Rounder", "Wicket Keeper", name="player_type"), nullable=False)
    points = Column(Integer, nullable=False)
    base_price = Column(Integer, nullable=False)
    is_sold = Column(Boolean, nullable=False, default=False)  
    sold_price = Column(Integer, nullable=True)  
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Foreign Keys
    auction_id = Column(Integer, ForeignKey("auctions.id", ondelete="CASCADE"))
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)



# Teams Model
class Team(Base):
    __tablename__ = "teams"    

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    remaining_purse = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Foreign Key
    auction_id = Column(Integer, ForeignKey("auctions.id", ondelete="CASCADE"))

    # Relationships
    players = relationship("Player")
    

# Summary Model
class Summary(Base):
    __tablename__ = "summary"

    id = Column(Integer, primary_key=True, nullable=False)
    sold_price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Foreign Keys
    auction_id = Column(Integer, ForeignKey("auctions.id", ondelete="CASCADE"))
    player_id = Column(Integer, ForeignKey("players.id", ondelete="SET NULL"))
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="SET NULL"))

    # Relationship
    players = relationship("Player")
    teams = relationship("Team")
    auction = relationship("Auction")

# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum("user", "team","admin", name="player_type"), nullable=False, default="user")
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)