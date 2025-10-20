import hashlib, subprocess, os
import concurrent.futures, asyncio
from typing import Tuple


def looks_like_shared_lib(path: str) -> bool:
    if not path:
        return False
    p = path.lower()
    return p.endswith(".dll")

def is_readable(path:str) ->  Tuple[bool, str]:
    if not path:
        return False, "empty path"
    if not os.path.exists(path):
        return False, "not found"
    if not os.path.isfile(path):
        return False, "not a file"
    if not os.access(path, os.R_OK):
        return False, "permission denied"
    return True, ''

def grab_sha256_hash_of_process(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

async def grab_sha256_async(file_path):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, grab_sha256_hash_of_process, file_path)

def is_signed(filepath: str) -> bool | str:
    signtool_path = os.path.join(os.path.dirname(__file__), "bin", "signtool.exe")
    try:
        result = subprocess.run(
            [signtool_path, "verify", "/pa", filepath],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True,
            check = False
        )
        output = result.stdout + result.stderr
        return "No signature found" not in output

    except FileNotFoundError:
        return "signtool.exe not found, must be in /bin folder"
    

def normalizing_score(score, max_score):
    return min(int((score / max_score) * 100), 100)

def analyze_score_risk(score: int) -> str:
    if score >= 80:
        return "critical"
    if score >= 50:
        return "warning"
    return "safe"
