import subprocess
import time
import requests
import cv2
from ultralytics import YOLO
import globals

from flask import Flask,request,jsonify

import os
app=Flask(__name__)
stop_detection =globals.stop
@app.route("/image", methods=["POST"])
def image_detection():
    try:
        model=YOLO(request.form.get('model_path'))
        image_path=request.form.get('image_path')
        print(image_path)
        frame = cv2.imread(image_path)
          
        if frame is None:
            print(" Error: Could not read image.")
            return

        
        results = model(frame, conf=0.1, imgsz=1280)
      
       
        annotated_frame = results[0].plot()

        cv2.imshow("Snack Detection", annotated_frame)
        # cv2.waitKey(0)
        
        os.makedirs("output", exist_ok=True)
        output_path = r"output\output_image.jpg"
        cv2.imwrite(r"output\output_image.jpg", annotated_frame)
        return {'output_path':output_path},200
    except(KeyboardInterrupt):
        print("Error: Keyboard interrupt detected. Exiting.")
    finally:
        print("Image detection completed successfully.")
        cv2.destroyAllWindows()

@app.route("/stop", methods=["POST"])
def stop_route():
    globals.stop = True
    return jsonify({"status": "stopped"})
@app.route("/startLabelStudio", methods=["POST"])
def start_label_studio():
    try:
        subprocess.Popen(['label-studio', 'start'])
        return jsonify({"status": "Label Studio started"}), 200
    except Exception as e:
        return str(e)

@app.route('/video', methods=['POST'])
def video_detection():
    all_detections = []
    try:
        
        video_path=request.form.get('video_path')
        model=YOLO(r"D:\image_processing\AISF-Webservice\model\best.pt")
        if not os.path.exists(video_path):
            path = r'output\output_video.mp4'
            if not os.path.exists(path):
                print("Error: Video file does not exist.")
                return
            video_path = path

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Error: Could not open video.")
            return

        
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        
        os.makedirs("output", exist_ok=True)
        output_path = r"output\output_video_detected.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while True:
            if globals.stop:
                print("Detection stopped by user.")
                cap.release()
                out.release()
                cv2.destroyAllWindows()
                print(f"Video detection completed successfully. Saved at: {output_path}")
                
                break
            ret, frame = cap.read()
            if not ret:
                print("End of video stream or cannot read the video.")
                break

            # Run detection
            results = model(frame, conf=0.1, imgsz=1280)
            annotated_frame = results[0].plot()

            all_detections.append(results[0].boxes)
            out.write(annotated_frame)

            
            cv2.imshow("Snack Detection", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Error: Keyboard interrupt detected. Exiting.")
    finally:
        os.makedirs("output", exist_ok=True)
        if all_detections:
            with open("output/output.txt", "w") as f:
                    for result in all_detections:
                        for box in result: # assuming ultralytics YOLOv8
                        # write detected class and confidence
                            f.write(f"{box.cls} {box.conf}\n")
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print(f"Video detection completed successfully. Saved at: {output_path}")

@app.route('/webcam', methods=['POST'])
def webcam_route():
    try:
        webcam_detection()
        return jsonify({"status": "Webcam detection started"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#Open web cam continously and generate 20 sec once a video
def webcam_detection(headless=True):
    count = 0

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Try opening camera
    cap = cv2.VideoCapture(0)  # Adjust index if needed
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    try:
        while True:
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            out_file = f'output/webcam_output_{count}.mp4'
            out = cv2.VideoWriter(out_file,
                                  cv2.VideoWriter_fourcc(*'mp4v'),
                                  30, (frame_width, frame_height))

            print(f"Recording chunk {count}...")

            for i in range(600):  # ~20 seconds at 30 fps
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame from webcam.")
                    break

                out.write(frame)

                # Sleep a tiny bit if needed to reduce CPU
                time.sleep(0.01)

            out.release()
            print(f"Saved {out_file}")
            count += 1

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
    finally:
        cap.release()
        print("Webcam detection completed successfully.")


def main():
    # model = YOLO(r"D:\img_processing_trial\img_processing_trial\kitkat_lays_kurkure.pt")
    model=YOLO(r"D:\image_processing\AISF-Webservice\model\best.pt")
    image_path=r"D:\image_processing\AISF-Webservice\test_input\welcome to America.jpg"
    img_link = requests.get("https://images.unsplash.com/photo-1632687380457-05a1271e873b?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHNuYWNrc3xlbnwwfHwwfHx8MA%3D%3D").content
    file_name='test_input.jpg'
    with open(file_name, 'wb') as f:
        f.write(img_link)
    
    
    webcam_detection()



 


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)
