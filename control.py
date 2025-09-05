import subprocess
import os
import signal
import time
process = None
def start_recorder():
    global process
    if process is None:
        process = subprocess.Popen(["python", "run_recorder_app.py"])
        print("✅ Recorder started")
    else:
        print("⚠️ Recorder already running")
def save_recordings_to_main():
    subprocess.run(["adb","pull","sdcard/Android/data/com.xy6126.recorder/files/Movies","C:\\Users\\riota\\Downloads"])
def stop_recorder():
    global process
    if process is not None:
        process.terminate()  
        process.wait()
        process = None
        print("🛑 Recorder stopped")
    else:
        print("⚠️ Recorder is not running")
if __name__ == "__main__":
    while True:
        cmd = input("Enter command (open/exit): ").strip().lower()
        if cmd == "open":
            start_recorder()
        
        elif cmd == "exit":
            time.sleep(30)  # Wait for 10 seconds before stopping
            print("Door closed ----> Saving recordings to main PC...")
            save_recordings_to_main()
            stop_recorder()
            break
        else:
            print("Unknown command")