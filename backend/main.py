import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import users, auth, clients, contracts, ad_campaigns, services, statistics

app = FastAPI(title="CRM System")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(contracts.router)
app.include_router(services.router)
app.include_router(ad_campaigns.router)
app.include_router(statistics.router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)