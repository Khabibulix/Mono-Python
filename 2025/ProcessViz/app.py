import pythoncom, asyncio
from quart import Quart, render_template
from process_manager import *

app = Quart(__name__)

process_cache = None

async def refresh_cache():
    global process_cache
    while True:
        try:
            data = await asyncio.to_thread(ProcessGetter.get_processes)
            process_cache = data
        except Exception as e:
            print("Cache error")
        await asyncio.sleep(3)

# For using WMI in Quart context
def run_wmi_function(fn, *args, **kwargs):
    pythoncom.CoInitialize()
    try:
        return fn(*args, **kwargs)
    finally:
        pythoncom.CoUninitialize()

@app.before_serving
async def startup():
    app.add_background_task(refresh_cache)

@app.route("/")
async def display_processes():
    if process_cache is None:
        return "⏳ Loading datas, you'll be kind to wait a bit...", 503
    return await render_template('index.html', get_processes=process_cache)


@app.route("/process/<int:pid>")
async def process_view(pid):
    def fetch_and_analyze():
        pythoncom.CoInitialize()
        try:
            infos = ProcessGetter.get_infos_for_process_with_pid(pid)
            if not infos:
                return None, None
            analyzer = ProcessAnalyzer(pid)
            result = analyzer.run()
            return infos, result
        finally:
            pythoncom.CoUninitialize()
    
    infos, result = await asyncio.to_thread(fetch_and_analyze)

    if not infos:
        return "Process not found", 404
    return await render_template('process.html', process_info=infos, result=result)

if __name__ == "__main__":
    app.run(debug=True)