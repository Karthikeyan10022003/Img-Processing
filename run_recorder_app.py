import subprocess
import time
def run_recorder_app():
    while True:
        subprocess.run(["adb","shell","am","force-stop","com.xy6126.recorder"])
        subprocess.run(["adb","shell","am","start","-n","com.xy6126.recorder/.MainActivity"])
        time.sleep(35)
    

   

def main():
    try:
        run_recorder_app()
    except KeyboardInterrupt:
        print("Door closed ----> Saving recordings to main PC...")
        
        print("Recorder app run interrupted by user.")
if __name__ == "__main__":
    main()