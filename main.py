import logging

from fastapi import FastAPI

from api.flows import router as flows_router
from api.user_flows import router as user_flows_router
from api.users import router as users_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="User & Flow API",
    version="1.0",
    description="API for managing users, flows, and user-flow relationships."
)

app.include_router(users_router)
app.include_router(flows_router)
app.include_router(user_flows_router)