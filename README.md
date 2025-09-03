# dashcam2gps

Extracts GPS tracks and speed from dashcam videos with embedded overlays, and exports them as a GPX file that can be loaded into mapping tools (Google Earth, Garmin, etc.).

## Features

- Supports dashcam videos with overlay text like `102KM/H N:53.8235 E:10.5033`
- Extracts:
  - Latitude / Longitude
  - Speed (km/h)
- Exports to **GPX 1.1** with speed included

## Example Output

```xml
<!-- ... -->
<trkpt lat="53.8235" lon="10.5033">
<extensions>
  <speed>102</speed>
</extensions>
</trkpt>
<!-- ... -->
```

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

## Roadmap

- Support for multiple dashcams
- Faster image recognition
- Parameters (units, sample count, region, output format, etc.)
- Allow multiple videos as input
- Track analysis