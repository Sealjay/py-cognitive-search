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
from azure.search import SearchApiKeyCredential, SearchIndexClient
from gensim.summarization import summarize

load_dotenv("./.env")

templates = Jinja2Templates(directory="templates")


def short_summary(text):
    token = "An Act to"
    if "An Act for" in text:
        token = "An Act for"
    if token in text and "[" in text:
        print("it's here")
        split_text = text.split(token)[1]
        split_text = split_text.split("[")
        purpose = f"{token} {split_text.pop(0)} "
        summary_text = purpose + summarize("[".join(split_text), word_count=30)
    else:
        summary_text = summarize(text, word_count=150)
    return summary_text


templates.env.filters["short_summary"] = short_summary


async def homepage(request):
    """Renders the default homepage."""
    await request.send_push_promise("/static/main.css")
    await request.send_push_promise("/favicon.ico")
    return templates.TemplateResponse("index.html", {"request": request})


async def search(request):
    """Renders the search results."""
    searchtext = request.query_params["searchtext"] or ""
    search_client = app.state.search_index_client
    searchresults = search_client.search(query=searchtext)
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "results": searchresults, "searchtext": searchtext},
    )


async def faq(request):
    """Renders the FAQ page."""
    return templates.TemplateResponse("faq.html", {"request": request})


async def error_template(request, exc):
    """Returns an error template and a message specific to the error case."""
    error_messages = {
        404: "Sorry, the page you're looking for isn't here.",
        500: "Server error.",
    }
    status_code = 500
    if hasattr(exc, "status_code"):
        status_code = exc.status_code

    if status_code in error_messages:
        error_message = error_messages[status_code]
    else:
        error_message = "No message saved for this error."
    return templates.TemplateResponse(
        "layout/error.html",
        {
            "request": request,
            "error_code": str(status_code),
            "error_message": error_message,
        },
    )


async def startup_get_search_client():
    credential = SearchApiKeyCredential(
        os.environ.get("AZURE_SEARCH_QUERY_KEY"),
    )
    client = SearchIndexClient(
        endpoint=os.environ.get("AZURE_SEARCH_ENDPOINT"),
        index_name=os.environ.get("AZURE_SEARCH_INDEX"),
        credential=credential,
    )
    app.state.search_index_client = client


routes = [
    Route("/", homepage),
    Route("/search", search, methods=["GET"]),
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
    on_startup=[startup_get_search_client],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", log_level="info")
