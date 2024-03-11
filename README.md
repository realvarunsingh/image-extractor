# Basic Cloud Vision Video Analysis

This Python script can be used to get labels from frames of a YouTube video using the Google Cloud Vision API, as a preprocessing step for using language models to analyze video content.
It captures frames (at a set interval) of a YouTube video at a specified resolution and analyzes them for labels (objects, activities, etc.).
Originally made for a CSE 291 final project.

## Prerequisites/Dependencies

Before you begin, ensure you have met the following requirements:

- Python 3.x installed (3.11 used for development)
- Google Cloud account with Vision API enabled: [quickstart guide for client libraries](https://cloud.google.com/vision/docs/detect-labels-image-client-libraries) is helpful
- Required Python packages: `cv2`, `numpy`, `yt_dlp`, `google-cloud-vision`

## Usage

To use the script, run it from the command line, passing arguments:

```
python cloud_vision_video_analysis.py <YouTube URL> [resolution] [number of frames to skip] [frame limit] [start frame]

```

You can also import the function `analyze_video_frames` to use in your own scripts.
