from fastapi import FastAPI
from app.register import router as register_router
from app.login import router as login_router
from app.add_transaction import router as add_transaction_router
from app.get_transactions import router as get_transactions_router


app = FastAPI()

app.include_router(register_router)
app.include_router(login_router)
app.include_router(add_transaction_router)
app.include_router(get_transactions_router)





