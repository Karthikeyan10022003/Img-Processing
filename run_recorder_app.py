import requests
# Flask endpoint for video detection
url = "http://127.0.0.1:5000/video"
# Path to the video you want to send
video_path = r"D:\img_processing_trial\img_processing_trial\output\webcam_output_0.mp4"
data= {'video_path': video_path}
response = requests.post(url, data=data)
# print(response.json())