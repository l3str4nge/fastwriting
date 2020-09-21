from fastapi import FastAPI

app = FastAPI(debug=True, redoc_url=None)


@app.post("/game/{username}/")
async def process_activity(user_ref: str,):
    error_message, period = await process_user_activity(User(user_ref), **dict(params))
    if error_message:
        response = {"detail": error_message, "period": period}
    else:
        response = {"detail": LIMIT_OK}

    return response