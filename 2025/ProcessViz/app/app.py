import os, asyncio
from quart import Quart
from app.setup_log import setup_logger
from app.ProcessGetter import ProcessGetter
from app.routes.views import views_bp
from app.routes.ws import ws_bp

base_dir = os.path.dirname(os.path.dirname(__file__))  # ProcessViz

app = Quart(
    __name__,
    template_folder=os.path.join(base_dir, "templates"),
    static_folder=os.path.join(base_dir, "static"),
    static_url_path="/static",
)

app.config["PROCESS_CACHE"] = None
logger = setup_logger(__name__)
app.logger = logger


async def refresh_cache():

    while True:
        try:
            data = await ProcessGetter.get_processes()
            app.config["PROCESS_CACHE"] = data
            logger.debug("First cached process: %s", list(data.items())[0])
            logger.debug("Process cache updated with %d entries", len(data))
        except Exception as e:
            logger.warning("Cache refresh error: %s", e)
        await asyncio.sleep(5)


@app.context_processor
def utility_processor():
    def basename(path):
        return os.path.basename(path)

    return dict(basename=basename)


@app.before_serving
async def startup():
    app.config["PROCESS_CACHE"] = await ProcessGetter.get_processes()
    app.add_background_task(refresh_cache)


app.register_blueprint(views_bp)
app.register_blueprint(ws_bp)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.set_debug(True)

    logger.info("Launching Quart app...")

    app.run(debug=False)
