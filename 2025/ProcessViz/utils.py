import hashlib, subprocess, os


def grab_sha256_hash_of_process(path_of_process):
    h = hashlib.sha256()
    with open(path_of_process, 'rb') as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def is_signed(filepath):
    signtool_path = os.path.join(os.path.dirname(__file__), "bin", "signtool.exe")
    try:
        result = subprocess.run(
            [signtool_path, "verify", "/pa", filepath],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True
        )
        output = result.stderr + result.stdout
        print(result)
        return False if "No signature found" in output else True

    except FileNotFoundError as fnfe:
        return "signtool.exe not found"