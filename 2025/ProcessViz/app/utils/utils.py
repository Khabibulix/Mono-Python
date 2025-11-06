import hashlib
import subprocess
import os
import asyncio


def hexdump(data: bytes, length: int = 16):
    result = []
    for i in range(0, min(len(data), 512), length):
        chunk = data[i : i + length]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        # Classic ASCII Chars, 32 is ' ' and 127 is '~'
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        result.append(f"{i:08x} {hex_part:<48} |{ascii_part}|")
    return result


def grab_sha256_hash_of_process(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        output = result.stdout + result.stderr
        return "No signature found" not in output

    except FileNotFoundError:
        return "signtool.exe not found, must be in /bin folder"


def normalizing_score(score, max_score):
    if score < 0:
        return 0
    return min(round((score / max_score) * 100), 100)


def analyze_score_risk(score: int) -> str:
    if score >= 80:
        return "critical"
    if score >= 50:
        return "warning"
    return "safe"


def estimate_risk_level(raw_metrics: dict) -> str:
    if not raw_metrics:
        return "unknown"

    risky_flags = [
        "path_suspicious",
        "path_deleted",
        "strange_chars",
        "not_bound_to_service",
        "invokes_python",
        "network_active",
    ]

    risk_points = sum(raw_metrics.get(flag, False) for flag in risky_flags)

    if not raw_metrics.get("is_signed", True):
        risk_points += 1

    if raw_metrics.get("path_trustworthy", False):
        risk_points -= 1

    if risk_points <= 1:
        return "low"
    elif risk_points <= 3:
        return "medium"
    else:
        return "high"
