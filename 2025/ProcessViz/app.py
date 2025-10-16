import pythoncom, asyncio
from quart import Quart, render_template, request
from process_manager import *

app = Quart(__name__)

# For using WMI in Quart context
def run_wmi_function(fn, *args, **kwargs):
    pythoncom.CoInitialize()
    try:
        return fn(*args, **kwargs)
    finally:
        pythoncom.CoUninitialize()

@app.route("/")
async def display_processes():
    processes = await asyncio.to_thread(get_processes)
    return await render_template('index.html', get_processes=processes)


@app.route("/process/<int:pid>", methods=["GET"])
async def process_view(pid):
    infos = await asyncio.to_thread(run_wmi_function, get_infos_for_process_with_pid, pid)
    result = await asyncio.to_thread(run_wmi_function, analyze_process, pid)
    return await render_template('process.html', get_processes=infos, result=result)

if __name__ == "__main__":
    app.run(debug=True)