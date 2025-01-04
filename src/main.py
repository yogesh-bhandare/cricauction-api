from fastapi import FastAPI
from .db.connect import engine
from .db.models import Base
from .auctions.routers import router as auction_router
from .players.routers import router as player_router
from .teams.routers import router as team_router
from .summary.routers import router as summary_router
from .auth.routers import router as login_router
from .user.routers import router as user_router
from .dashboard.routers import router as dashboard_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(login_router)
app.include_router(auction_router)
app.include_router(team_router)
app.include_router(player_router)
app.include_router(dashboard_router)
app.include_router(summary_router)
