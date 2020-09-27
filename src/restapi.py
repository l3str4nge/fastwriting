from fastapi import FastAPI, Depends
from uuid import uuid1

from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.game.game import Game, Stage

app = FastAPI(debug=True, redoc_url=None)


@app.post("/game/{username}/")
async def new_game(username: str, session: Session = Depends(get_db)):
    game = await Game.create_for(username)
    stage = await Stage.create(session, None, game['current_stage'])
    return {
        'game': game,
        'stage': stage
    }
