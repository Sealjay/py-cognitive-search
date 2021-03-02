import os
from dotenv import load_dotenv
import uvicorn
from starlette.applications import Starlette
from starlette.responses import (
    Response,
    FileResponse,
)
from starlette.staticfiles import StaticFiles
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware

templates = Jinja2Templates(directory="templates")
load_dotenv("./.env")


async def homepage(request):
    """Renders the default homepage."""
    await request.send_push_promise("/static/main.css")
    await request.send_push_promise("/favicon.ico")
    return templates.TemplateResponse("index.html", {"request": request})


async def faq(request):
    """Renders the FAQ page."""
    return templates.TemplateResponse("faq.html", {"request": request})


async def startup_get_video_indexer():
    app.state.video_indexer = await AsyncVideoIndexer.AsyncVideoIndexer.create(
        os.environ.get("VIDEO_INDEXER_ACCOUNT_ID"),
        os.environ.get("VIDEO_INDEXER_KEY"),
        os.environ.get("VIDEO_INDEXER_ACCOUNT_LOCATION"),
    )


async def error_template(request, exc):
    """Returns an error template and a message specific to the error case."""
    error_messages = {
        404: "Sorry, the page you're looking for isn't here.",
        500: "Server error.",
    }
    if exc.status_code in error_messages:
        error_message = error_messages[exc.status_code]
    else:
        error_message = "No message saved for this error."
    return templates.TemplateResponse(
        "layout/error.html",
        {
            "request": request,
            "error_code": str(exc.status_code),
            "error_message": error_message,
        },
    )


routes = [
    Route("/", homepage),
    Route("/faq", faq),
    Route("/favicon.ico", FileResponse("static/favicon.ico")),
    Mount(
        "/static",
        app=StaticFiles(directory="static"),
        name="static",
    ),
]

middleware = [
    Middleware(GZipMiddleware, minimum_size=500),
    Middleware(
        uvicorn.middleware.proxy_headers.ProxyHeadersMiddleware, trusted_hosts="*"
    ),
]

exception_handlers = {404: error_template, 500: error_template}

if os.getenv("DEBUG", None) is None:
    debug = False
else:
    debug = True


app = Starlette(
    debug=debug,
    routes=routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
    # on_startup=[startup_get_video_indexer],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", log_level="info")
