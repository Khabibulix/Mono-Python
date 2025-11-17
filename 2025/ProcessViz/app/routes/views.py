import asyncio

from quart import Blueprint, render_template, request, abort, current_app
from urllib.parse import unquote_plus
from app.setup_log import setup_logger


from app.utils.utils_process import is_readable, build_process_tree, fetch_and_analyze
from app.utils.utils import hexdump
from app.utils.utils_dll import read_file_chunk, extract_ascii_strings, parse_pe_info


views_bp = Blueprint("views", __name__)
logger = setup_logger(__name__)


@views_bp.route("/")
async def display_processes():
    return await render_template("index.html")


@views_bp.route("/process/<int:pid>")
async def process_view(pid):
    infos, result = await fetch_and_analyze(pid)
    if not infos:
        return "Process not found", 404
    return await render_template("process.html", process_info=infos, result=result)


@views_bp.route("/tree")
async def display_process_tree():
    cache = current_app.config["PROCESS_CACHE"]

    if not cache:
        logger.warning("Cache not ready when accessing /tree")
        return await render_template("loading.html"), 503

    processes_by_pid = {v["PID"]: v for v in cache.values()}

    logger.debug("Building process tree from %d processes", len(processes_by_pid))

    try:
        tree = build_process_tree(processes_by_pid)
    except Exception as e:
        logger.exception("Error building process tree")
        return "Internal error while building tree", 500

    return await render_template("tree.html", process_tree=tree)


@views_bp.route("/process/<int:pid>/dll")
async def dll_view(pid):
    path = request.args.get("path")
    logger.info(f"Analysing {path} DLL")
    if not path:
        abort(400, "Missing path param")
    path = unquote_plus(path)

    readable, error = is_readable(path)
    if not readable:
        abort(403, f"Cannot access DLL: {error}")

    try:
        data = await asyncio.to_thread(read_file_chunk, path)
    except Exception as e:
        abort(500, f"Error reading file: {e}")

    strings = extract_ascii_strings(data)
    hex_lines = hexdump(data)

    try:
        dll_info = await asyncio.to_thread(parse_pe_info, path)
    except Exception as e:
        logger.info(f"PE parsing failed: {e}")
        dll_info = {}

    return await render_template(
        "dll.html",
        pid=pid,
        path=path,
        strings=strings,
        hexdump=hex_lines,
        dll_info=dll_info,
    )


@views_bp.route("/api/processes")
async def api_get_processes():
    cache = current_app.config["PROCESS_CACHE"]

    if not cache:
        return {"status": "loading", "data": []}, 503

    top = sorted(
        cache.items(),
        key=lambda item: float(item[1].get("memory_percent", 0) or 0),
        reverse=True,
    )[:20]

    light_cache = {
        name: {
            "Name": proc.get("name"),
            "PID": proc.get("PID"),
            "Memory Usage": proc.get("memory_percent"),
            "Status": proc.get("status"),
            "Time Alive": proc.get("time_alive"),
        }
        for name, proc in top
    }
    return {"status": "ok", "data": light_cache}
