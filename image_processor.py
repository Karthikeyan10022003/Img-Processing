import requests
import cv2
from ultralytics import YOLO
import os
def image_detection(model, image_path):
    try:
  
        frame = cv2.imread(image_path)

        if frame is None:
            print(" Error: Could not read image.")
            return

        
        results = model(frame, conf=0.1, imgsz=1280)
      
       
        annotated_frame = results[0].plot()

        cv2.imshow("Snack Detection", annotated_frame)
        cv2.waitKey(0)
        
        os.makedirs("output", exist_ok=True)
        
        cv2.imwrite(r"output\output_image.jpg", annotated_frame)
    except(KeyboardInterrupt):
        print("Error: Keyboard interrupt detected. Exiting.")
    finally:
        print("Image detection completed successfully.")
        cv2.destroyAllWindows()

def video_detection(model, video_path):
    try:
        if not os.path.exists(video_path):
            path=r'output\output_video.mp4'
            if not os.path.exists(path):
                print("Error: Video file does not exist.")
                return
            video_path=path
            
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Error: Could not open video.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("End of video stream or cannot read the video.")
                break

            results = model(frame, conf=0.1, imgsz=1280)
            annotated_frame = results[0].plot()

            cv2.imshow("Snack Detection", annotated_frame)
            cv2.imwrite(r"output\output_video_frame.jpg", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except(KeyboardInterrupt):
        print("Error: Keyboard interrupt detected. Exiting.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Video detection completed successfully.")
#Open web cam continously and generate 20 sec once a video
def webcam_detection():
    count=0
    try:
        while True:
            cap=cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Could not open webcam.")
                return
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            out = cv2.VideoWriter(f'output/webcam_output_{count}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))
            for i in range(600):
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame from webcam.")
                    break

                
                out.write(frame)

                cv2.imshow("Snack Detection", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            out.release()
            count+=1
    except(KeyboardInterrupt):
        print("Error: Keyboard interrupt detected. Exiting.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam detection completed successfully.")


def main():
    model = YOLO(r"D:\img_processing_trial\img_processing_trial\kitkat_lays_kurkure.pt")
    # model=YOLO(r"C:\Users\riota\Downloads\best.pt")
    image_path=r"D:\img_processing_trial\img_processing_trial\welcome to America.jpg"
    img_link = requests.get("https://images.unsplash.com/photo-1632687380457-05a1271e873b?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHNuYWNrc3xlbnwwfHwwfHx8MA%3D%3D").content
    file_name='test_input.jpg'
    with open(file_name, 'wb') as f:
        f.write(img_link)
    
    # image_detection(model, file_name)
    video_detection(model,r'D:\img_processing_trial\img_processing_trial\istockphoto-2179808994-640_adpp_is.mp4')



 


if __name__ == "__main__":
    main()
