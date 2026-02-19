import asyncio
import json
import httpx
import subprocess
import time
import sys
import os
import signal

# Add src to path
sys.path.append(".")

async def test_stream():
    print("Starting API Server via subprocess...")
    # Run uvicorn as a separate process
    cmd = [sys.executable, "-m", "uvicorn", "src.api.app:app", "--host", "127.0.0.1", "--port", "8001"]
    proc = subprocess.Popen(cmd, cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(5)
    
    url = "http://127.0.0.1:8001/task/stream"
    payload = {"query": "Test query for streaming"}
    
    print(f"Connecting to {url}...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                print("Connected! Receiving events:")
                if response.status_code != 200:
                    print(f"Error: Server returned {response.status_code}")
                    return

                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            print("\nStream finished successfully.")
                            break
                        try:
                            json_data = json.loads(data)
                            print(f"Event: {json_data.keys()}")
                        except:
                            print(f"Raw: {data}")
    except Exception as e:
        print(f"Test Failed: {e}")
        # Print server output for debugging
        if proc.poll() is not None:
            stdout, stderr = proc.communicate()
            print(f"Server STDOUT: {stdout.decode()}")
            print(f"Server STDERR: {stderr.decode()}")
    finally:
        print("Stopping server...")
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()

if __name__ == "__main__":
    asyncio.run(test_stream())
