import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Crypto(BaseModel):
    name: str
    price: int


db = {
    1: Crypto(name="TrumpCoin", price=8000000),
    2: Crypto(name="FPIBank", price=88888888),
    3: Crypto(name="Bitcoin", price=10000000),
}


@app.get("/")
def read_root():
    return {
        "Hello": "FastAPI"
    }


@app.get("/crypto/{crypto_id}")
def get_crypto(crypto_id: int) -> Crypto:
    if crypto_id not in db:
        raise HTTPException(status_code=404, detail='Not found.')
    return db[crypto_id]


@app.post("/crypto/{crypto_id}")
def create_crypto(crypto: Crypto) -> Crypto:
    crypto_id = max(db.keys()) + 1 if db else 1
    db[max(db.keys()) + 1] = crypto
    return crypto


@app.put("/crypto/{crypto_id}")
def update_crypto(crypto_id: int, new_price: int):
    if crypto_id not in db:
        raise HTTPException(status_code=404, detail='Not found.')

    db[crypto_id].price = new_price
    return db[crypto_id]


@app.delete("/crypto")
def delete_crypto(crypto_id: int):
    if crypto_id not in db:
        raise HTTPException(status_code=404, detail='Not found.')

    del db[crypto_id]
    return HTTPException(status_code=200, detail='Crypto deleted.')


uvicorn.run(app)
