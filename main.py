import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.staticfiles import RedirectResponse, StaticFiles

import models
from database import engine
from routers import auth, todos, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")


# To redirect all to /todos
@app.get("/")
async def root():
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
