# some code from https://stackoverflow.com/questions/50876292/capture-youtube-video-
# for-further-processing-without-downloading-the-video

import sys
import os
import shutil

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

def capture_frames(video_url, skip_frames, max_frames):
    """
    Capture a frame every 'skip_frames' frames from a video.

    Args:
        video_url (str): URL of the video to capture frames from.
        skip_frames (int): The number of frames to skip before capturing the next frame.

    Returns:
        bool: True if frames were captured and saved successfully, False otherwise.
    """
    if not os.path.exists('frames'):
        os.makedirs('frames')

    cap = cv2.VideoCapture(video_url)
    if not cap.isOpened():
        print('Video not opened')
        return False

    frame_count = 0
    saved_frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # temp files created so images don't fill up RAM in cases of very long videos/high resolution
        if frame_count % skip_frames == 0:
            frame_filename = f'frames/frame_{frame_count}.jpg'
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1

        frame_count += 1
        if saved_frame_count >= max_frames:
            break

    cap.release()

    if saved_frame_count == 0:
        print('No frames captured')
        return False

    return True

def analyze_frame_labels():
    """
    Analyze the saved frames for labels using Google Vision API.

    Returns:
        dict: A dictionary where keys are frame filenames and values are lists of labels detected in each frame.
    """
    client = vision.ImageAnnotatorClient()
    frames_labels = []
    for frame_filename in os.listdir('frames'):
        if frame_filename.endswith('.jpg'):
            with open(f'frames/{frame_filename}', 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            response = client.label_detection(image=image)
            labels = response.label_annotations
            frames_labels.append((frame_filename, [label.description for label in labels]))
    shutil.rmtree('frames')
    return frames_labels

def analyze_video_frames(video_url, resolution, skip_frames, max_frames):
    """
    Analyze the frames of a video for labels using Google Vision API.

    Args:
        video_url (str): URL of the video to analyze.

    Returns:
        list: A list of labels detected in the frames of the video.
    """
    url_240p = get_video_url(video_url, resolution)
    if url_240p and capture_frames(url_240p, skip_frames, max_frames):
        labels = analyze_frame_labels()
        return labels
    else:
        return []

if __name__ == '__main__':
    import pprint # for visually pleasing printing

    # Example usage
    video_url = sys.argv[1]
    resolution = sys.argv[2] if len(sys.argv) > 2 else '240p'
    skip_frames = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    max_frames = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    assert skip_frames > 0, "skip_frames must be greater than 0"
    assert max_frames > 0, "max_frames must be greater than 0"

    labels = analyze_video_frames(video_url, resolution, skip_frames, max_frames)
    pprint.pp(labels)
