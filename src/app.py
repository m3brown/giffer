from cache import cache
from fastapi import BackgroundTasks
from fastapi import FastAPI
from fileremover import remove_file
from gif_factory import GifFactory
import giphy
from models import GifRequest
from starlette.responses import FileResponse
from starlette.responses import HTMLResponse

app = FastAPI()

factory = GifFactory()


@app.on_event("startup")
async def startup_event():
    await cache.startup()


@app.on_event("shutdown")
async def shutdown_event():
    await cache.close()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
      <html>
        <head><title>Giffer</title></head>
        <body>
          <br>
          <center>
            Please refer to the <a href="/docs">documentation</a> for guidance.
          </center>
        </body>
      </html>
    """


@app.post("/")
async def giffer(data: GifRequest, background_tasks: BackgroundTasks):
    if data.search:
        url = await giphy.search(data.search)
        data = data.copy(update={"gif": url.decode("utf-8")})

    gif_file_path = await factory.create(data)
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
    }
    background_tasks.add_task(remove_file, gif_file_path)
    return FileResponse(path=gif_file_path, headers=headers, media_type="image/gif")
