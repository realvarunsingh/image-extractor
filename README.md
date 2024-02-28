# Basic Cloud Vision Video Analysis

This Python script, `cloud_vision_video_analysis.py can be used for analyzing video frames using Google Cloud Vision API.
It captures the first frame of a YouTube video at a specified resolution, analyzes it for labels (objects, activities, etc.), and returns those labels. (this will be expanded to every x frames, labels will be returned in a set)
Originally made for a CSE 291 final project.

## Prerequisites/Dependencies

Before you begin, ensure you have met the following requirements:

- Python 3.x installed (3.11 used for development)
- Google Cloud account with Vision API enabled: [quickstart guide for client libraries](https://cloud.google.com/vision/docs/detect-labels-image-client-libraries) is helpful
- Required Python packages: `cv2`, `numpy`, `yt_dlp`, `google-cloud-vision`

## Usage

To use the script, run it from the command line, passing the YouTube video URL as an argument:

```
python main.py <YouTube URL>

```

You can also import the function `analyze_video_frame` to use in your own scripts.
