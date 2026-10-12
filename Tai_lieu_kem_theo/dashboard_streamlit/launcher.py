"""Start the dashboard with project-local dependencies on D/E."""
import argparse
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parent


def project_environment():
    if ROOT.drive.upper() not in {"D:", "E:"}:
        raise RuntimeError("Hãy giải nén thư mục dashboard vào ổ D hoặc E rồi mở lại.")
    runtime = ROOT / ".runtime"
    paths = {
        "TEMP": runtime / "temp", "TMP": runtime / "temp",
        "PIP_CACHE_DIR": runtime / "pip-cache", "PYTHONPYCACHEPREFIX": runtime / "pycache",
        "USERPROFILE": runtime / "profile", "APPDATA": runtime / "profile/AppData/Roaming",
        "LOCALAPPDATA": runtime / "profile/AppData/Local",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update({key: str(value) for key, value in paths.items()})
    env.update(PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1",
               STREAMLIT_BROWSER_GATHER_USAGE_STATS="false",
               STREAMLIT_SERVER_HEADLESS="true", STREAMLIT_SERVER_SHOW_EMAIL_PROMPT="false")
    # Read the same clean CSV that the notebook writes in the project folder.
    env["MARKETING_DATA_FILE"] = str(ROOT.parent.parent / "marketing_clean_powerbi.csv")
    return env


def dependencies_ready(python, env):
    code = "import importlib.metadata as m; print('|'.join(m.version(n) for n in ('streamlit','plotly','pandas')))"
    result = subprocess.run([str(python), "-c", code], env=env, capture_output=True, text=True)
    return result.returncode == 0 and result.stdout.strip() == "1.65.0|6.9.0|3.0.1"


def get_runtime(env, explicit=None):
    if explicit:
        python = Path(explicit).resolve()
        if not dependencies_ready(python, env):
            raise RuntimeError("Môi trường được chỉ định chưa có các phiên bản trong requirements.txt.")
        return python
    if sys.version_info < (3, 11):
        raise RuntimeError("Cần Python 3.11 trở lên. Bản này đã kiểm tra với Python 3.12.")
    python = ROOT / ".venv/Scripts/python.exe"
    if not python.exists():
        print("Đang chuẩn bị môi trường riêng trong thư mục dashboard…", flush=True)
        subprocess.run([sys.executable, "-m", "venv", str(ROOT / ".venv")], env=env, check=True)
    if not dependencies_ready(python, env):
        print("Đang cài thư viện. Lần đầu cần kết nối Internet…", flush=True)
        subprocess.run([str(python), "-m", "pip", "install", "--disable-pip-version-check",
                        "-r", str(ROOT / "requirements.txt")], env=env, check=True)
    if not dependencies_ready(python, env):
        raise RuntimeError("Thư viện chưa cài đủ. Kiểm tra kết nối Internet rồi mở lại.")
    return python


def free_port():
    for port in range(8510, 8531):
        with socket.socket() as sock:
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise RuntimeError("Các cổng chạy dashboard đang bận. Đóng cửa sổ dashboard cũ rồi mở lại.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--runtime-python", help=argparse.SUPPRESS)
    options = parser.parse_args()
    env = project_environment()
    python = get_runtime(env, options.runtime_python)
    check = "from pathlib import Path; from data_model import read_snapshot,statistics; import json,os; print(json.dumps(statistics(read_snapshot(Path(os.environ['MARKETING_DATA_FILE'])).frame)))"
    result = subprocess.run([str(python), "-c", check], env=env, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError("Chưa đọc được CSV sạch. Kiểm tra file marketing_clean_powerbi.csv trong thư mục bài làm.\n" + result.stderr)
    if options.check_only:
        print(result.stdout.strip())
        return
    port = free_port()
    url = f"http://127.0.0.1:{port}"
    print(f"Dashboard: {url}\nGiữ cửa sổ này mở. Nhấn Ctrl+C để dừng.", flush=True)
    process = subprocess.Popen([str(python), "-m", "streamlit", "run", str(ROOT / "app.py"),
                                "--server.address=127.0.0.1", f"--server.port={port}"],
                               cwd=ROOT, env=env)
    try:
        for _ in range(80):
            if process.poll() is not None:
                raise RuntimeError("Dashboard chưa khởi động được. Xem thông báo phía trên.")
            try:
                with urllib.request.urlopen(url + "/_stcore/health", timeout=1) as response:
                    if response.status == 200:
                        break
            except (OSError, urllib.error.URLError):
                time.sleep(0.25)
        else:
            raise RuntimeError("Dashboard chưa sẵn sàng sau thời gian chờ. Mở lại để thử.")
        if not options.no_browser:
            webbrowser.open(url)
        process.wait()
    except KeyboardInterrupt:
        pass
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=10)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError, OSError) as exc:
        print(f"\nChưa chạy được dashboard: {exc}", file=sys.stderr)
        sys.exit(1)
