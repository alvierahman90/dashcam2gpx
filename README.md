# dashcam2gpx

> [!NOTE]
>
> Your dashcam footage may already come with GPS information already embedded!
> Try the provided [`extract_gpx.sh`](./extract_gpx.sh) script before using `dashcam2gpx.py`.
> It will be more accurate and run much faster.
> `extract_gpx.sh` requires exiftool to be installed on your system.
> Usage:
>
> ```
> ./extract_gpx.sh FILE1 [FILE2 [FILE3 [...]]]
> ```
>

Extract GPS tracks and speed from dashcam videos with embedded overlays,
and export them as a GPX file that can be loaded into mapping tools (Google Earth, Garmin, etc.).

## Features

- Supports dashcam videos with overlay text like `102KM/H N:53.8235 E:10.5033`
- Extracts:
  - Latitude / Longitude
  - Speed
- Exports to **GPX 1.1** with speed included

## Installation

1. Clone the repo.

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract).

## Usage example

```bash
python extract.py video.mp4 -o data.gpx -s 10
```

## Notes

- Adjust sample_seconds (lower = more precise track, higher = faster processing) to your liking.
- Crop region may need adjustment depending on your dashcam overlay location. I am using a VIOFO A229 Pro, the region might be different for your dashcam!
- Preprocessing is applied for better OCR accuracy.
