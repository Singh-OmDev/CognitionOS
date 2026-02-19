import subprocess
import time
import os
import signal
import sys
import threading

def stream_output(process, prefix):
    for line in iter(process.stdout.readline, ""):
        print(f"[{prefix}] {line.strip()}")
    process.stdout.close()

def main():
    print("Starting CognitionOS System...")
    
    # 1. Start Backend
    print("Launching Backend (FastAPI)...")
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.api.app:app", "--reload", "--host", "127.0.0.1", "--port", "8000"],
        stdout=sys.stdout,
        stderr=sys.stderr, # Share stderr
        cwd=os.getcwd(),
        shell=False # Shell not needed when calling python executable directly usually, easier to kill too
    )

    # 2. Start Frontend
    print("Launching Frontend (Next.js)...")
    frontend_cwd = os.path.join(os.getcwd(), "web")
    # Using npm run dev. On Windows we need shell=True or use "npm.cmd"
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    
    frontend = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        stdout=sys.stdout,
        stderr=sys.stderr,
        cwd=frontend_cwd,
        shell=True
    )

    print("\nSystem Running:")
    print("- Backend: http://localhost:8000")
    print("- Frontend: http://localhost:3000")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)
            if backend.poll() is not None:
                print("Backend process ended unexpectedly.")
                break
            if frontend.poll() is not None:
                print("Frontend process ended unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\nStopping services...")
    finally:
        # Terminate processes
        if backend.poll() is None:
            backend.terminate()
        if frontend.poll() is None:
            # npm often spawns child processes, simple terminate might not kill all. 
            # But for dev script this is usually acceptable.
             # On Windows, terminate() might not work well with shell=True processes.
            subprocess.call(["taskkill", "/F", "/T", "/PID", str(frontend.pid)])
        
        if backend.poll() is None:
             subprocess.call(["taskkill", "/F", "/T", "/PID", str(backend.pid)])

        print("Services stopped.")

if __name__ == "__main__":
    main()
