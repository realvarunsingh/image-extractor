# some code from https://stackoverflow.com/questions/50876292/capture-youtube-video-
# for-further-processing-without-downloading-the-video

import sys
import os

import cv2
import numpy as np
import yt_dlp as youtube_dl
from google.cloud import vision

def get_video_url(video_url, format_note='240p'):
    """
    Get the video URL for a specific format.
    
    Args:
        video_url (str): URL of the video to get the format URL from.
        format_note (str): The desired video format.
    
    Returns:
        str: The URL of the video in the specified format, or None if not found.
    """
    ydl_opts = {}
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    info_dict = ydl.extract_info(video_url, download=False)
    formats = info_dict.get('formats', None)

    # get first format with required note
    for f in formats:
        if f.get('format_note', None) == format_note:
            return f.get('url', None)
    
    return None

def capture_first_frame(video_url):
    """
    Capture the first frame of a video.
    
    Args:
        video_url (str): URL of the video to capture the frame from.
    
    Returns:
        bool: True if the frame was captured and saved successfully, False otherwise.
    """
    cap = cv2.VideoCapture(video_url)
    if not cap.isOpened():
        print('Video not opened')
        return False

    ret, frame = cap.read()
    if not ret:
        print('No frame captured')
        return False

    cv2.imwrite('temp_first_frame.jpg', frame)
    cap.release()
    return True

def analyze_frame_labels():
    """
    Analyze the saved frame for labels using Google Vision API.
    
    Returns:
        list: A list of labels detected in the frame.
    """
    client = vision.ImageAnnotatorClient()
    with open('temp_first_frame.jpg', 'rb') as image_file:
        content = image_file.read()
    os.remove('temp_first_frame.jpg')
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    return [label.description for label in labels]

def analyze_video_frame(video_url):
    """
    Analyze the first frame of a 240p video for labels using Google Vision API.
    
    Args:
        video_url (str): URL of the video to analyze.
    
    Returns:
        list: A list of labels detected in the first frame of the video.
    """
    url_240p = get_video_url(video_url, '240p')
    if url_240p and capture_first_frame(url_240p):
        labels = analyze_frame_labels()
        return labels
    else:
        return []

if __name__ == '__main__':
    # Example usage of functions
    video_url = sys.argv[1]
    labels = analyze_video_frame(video_url)

    # Print in a line
    print("\nLabels: ")
    for label in labels:
        print(label, end=' ')
    print()


