from backend.api.v1.views import auth
from backend.main import app

app.include_router(auth.router)
