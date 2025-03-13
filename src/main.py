from fastapi import FastAPI
from database import init_models
from routers import post
from routers import user


app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_models() 





app.include_router(user.router)
app.include_router(post.router)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
