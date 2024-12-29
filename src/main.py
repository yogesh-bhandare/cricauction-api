from fastapi import FastAPI
from .db.connect import engine
from .db.models import Base
from .auctions.routers import router as auction_router
from .players.routers import router as player_router
from .teams.routers import router as team_router
from .summary.routers import router as summary_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auction_router)
app.include_router(player_router)
app.include_router(team_router)
app.include_router(summary_router)
