"""
main
"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from src.configs.constants import APP_CONTEXT_PATH
from src.versions.v1 import main as v1_route
from src.configs.env import get_settings

config = get_settings()


app = FastAPI(
    title="Demo Application",
    description="This application will serve APIs for TEST APP",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include version routers
app.include_router(v1_route.api_router, prefix=APP_CONTEXT_PATH)

# for routes in app.routes:
#     print(routes.path_regex.pattern)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
