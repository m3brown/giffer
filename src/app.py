from cache import cache
from fastapi import BackgroundTasks
from fastapi import FastAPI
from fastapi import Form
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
          <div>
              <form action="/form" method='POST'>
                  <input name='search'>
                  <input name='text'>
                  <input value="Submit" type="submit">
              </form>
          </div>
        </body>
      </html>
    """


async def process_gif_request(data: GifRequest, background_tasks: BackgroundTasks):
    if data.search:
        url = await giphy.search(data.search)
        if type(url) == bytes:
            url = url.decode("utf-8")
        data = data.copy(update={"gif": url})

    gif_file_path = await factory.create(data)
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
    }
    background_tasks.add_task(remove_file, gif_file_path)
    return FileResponse(path=gif_file_path, headers=headers, media_type="image/gif")


@app.post("/")
async def giffer(data: GifRequest, background_tasks: BackgroundTasks):
    return await process_gif_request(data, background_tasks)


@app.post("/form")
async def giffer_form(
    background_tasks: BackgroundTasks, search: str = Form(...), text: str = Form(...)
):
    data = GifRequest(search=search, text=text)
    return await process_gif_request(data, background_tasks)
