import subprocess
import tempfile


def analyze(code: str, language: str):
    if language.lower() != "python":
        return "Static analysis currently supports Python only."

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
        f.write(code)
        filename = f.name

    result = subprocess.run(
        ["pylint", filename, "--disable=all", "--enable=E,W"],
        capture_output=True,
        text=True
    )

    return result.stdout
