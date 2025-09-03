import subprocess
import time
def run_recorder_app():
    subprocess.run(["adb","shell","am","start","-S","-n","com.xy6126.recorder/.MainActivity"])
def save_recordings_to_main():
    subprocess.run(["adb","pull","sdcard/Android/data/com.xy6126.recorder/files/Movies","C:\\Users\\riota\\Downloads"])
def main():
    try:
        run_recorder_app()
    except KeyboardInterrupt:
        save_recordings_to_main()
        print("Recorder app run interrupted by user.")
if __name__ == "__main__":
    main()