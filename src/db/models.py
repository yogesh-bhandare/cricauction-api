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
    purse_amt = Column(Integer, nullable=False) # The amt that teams will be allocated for bid
    min_bid = Column(Integer, nullable=True) # if player bid is smaller then this then this bid will be considered or starting bid
    bid_increase_by = Column(Integer, nullable=False) # increase bid amt
    bid_amt = Column(Integer, nullable=True) # If this bid amt exceeds the new bid amt will get assigned
    new_bid_increase_by = Column(Integer, nullable=True) # this is the new bid amt
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, onupdate=func.now(), default=func.now())

    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

# Players Model
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    img_url = Column(String, nullable=True)
    origin = Column(Enum("Overseas", "Native", name="player_origin"), nullable=False, default="Native")
    player_type = Column(Enum("Batsman", "Bowler","All Rounder", "Wicket Keeper", name="player_type"), nullable=False)
    points = Column(Integer, nullable=False) # points for final results and player stats
    base_price = Column(Integer, nullable=False) # starting bid price
    is_sold = Column(Boolean, nullable=False, default=False) # status to get players sold details
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
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True) # for team login route
    auction_id = Column(Integer, ForeignKey("auctions.id", ondelete="CASCADE"))

    

# Summary Model
class Summary(Base):
    __tablename__ = "summary"

    id = Column(Integer, primary_key=True, nullable=False)
    sold_price = Column(Integer, nullable=False) # for security storing player sold_price
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Foreign Keys
    auction_id = Column(Integer, ForeignKey("auctions.id", ondelete="CASCADE")) # which auction
    player_id = Column(Integer, ForeignKey("players.id", ondelete="SET NULL")) # which player sold
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="SET NULL")) # which team bought

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
    role = Column(Enum("admin", "user", "team", name="role"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

