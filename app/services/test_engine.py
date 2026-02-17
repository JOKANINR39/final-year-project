import subprocess
import tempfile
import time


def run_tests(code: str):
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
        f.write(code)
        filename = f.name

    start = time.time()

    try:
        result = subprocess.run(
            ["python", filename],
            capture_output=True,
            text=True,
            timeout=5
        )

        execution_time = round(time.time() - start, 4)

        return {
            "output": result.stdout,
            "error": result.stderr,
            "execution_time": execution_time,
            "status": "Success" if result.returncode == 0 else "Failed"
        }

    except Exception as e:
        return {
            "output": "",
            "error": str(e),
            "execution_time": 0,
            "status": "Error"
        }
