from ckiptagger import WS, POS, NER
from fastapi import FastAPI

from .routers import default

app = FastAPI(
    title='CKIP Service',
    description='Web service for ckiplab/ckiptagger'
)
# model variables
app.ws = None
app.pos = None
app.ner = None


@app.on_event('startup')
async def initial() -> None:
    # Load model
    app.ws = WS('./data')
    app.pos = POS('./data')
    app.ner = NER('./data')


app.include_router(default.router)
