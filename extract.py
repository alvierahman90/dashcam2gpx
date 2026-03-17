# -*- coding: utf-8 -*-
import cv2
import pytesseract
import re
import xml.etree.ElementTree as ET
import argparse
import os

# TODO: optimize this regex
pattern = re.compile(
    r"(\d+)\s*(MPH|KM/H|KPH)\s*([NS])[: ]?(\d+\.\d+)\s*([EW])[: ]?(\d+\.\d+)"
)


def extract_gps_from_video(
    video_path, output_gpx, track_name, sample_seconds=5, max_speed=None
):
    """
    Extract GPS and speed from dashcam video overlay and save as GPX.
    :param video_path: path to dashcam MP4 file
    :param output_gpx: output GPX file path
    :param sample_seconds: interval (in seconds) between frames to analyze
    """
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # fallback value
    frame_interval = int(fps * sample_seconds)

    frame_count = 0
    results = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w, _ = frame.shape
        cropped = frame[h - 50 : h - 20, 20:500]

        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

        print(
            f"processing {100*frame_count/total_frames:.2f}%: {frame_count=} ", end=""
        )

        try:
            text = pytesseract.image_to_string(
                thresh,
                config="--psm 7 -c tessedit_char_whitelist=0123456789.SNEWKM/HP ",
            )
        except Exception as e:
            print("Exception running OCR: {e=}")
            continue

        print(f"{text=} ", end="")

        gps_match = pattern.search(text)

        if gps_match:
            speed, speed_unit, northsouth, lat, eastwest, lon = gps_match.groups()
            speed, lat, lon = int(speed), float(lat), float(lon)

            if max_speed and speed > max_speed:
                speed = None

            if northsouth == "S":
                lat = -lat
            if eastwest == "W":
                lon = -lon

            print(f"{lat=} {lon=} {speed=} {speed_unit=}")
            results.append((lat, lon, speed))
        else:
            print("no match :(")

        frame_count += frame_interval
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)

    cap.release()

    gpx = ET.Element("gpx", version="1.1", creator="dashcam2gpx")
    trk = ET.SubElement(gpx, "trk")
    name = ET.SubElement(trk, "name")
    name.text = track_name
    trkseg = ET.SubElement(trk, "trkseg")

    for lat, lon, speed in results:
        trkpt = ET.SubElement(trkseg, "trkpt", lat=str(lat), lon=str(lon))
        if speed is not None:
            ext = ET.SubElement(trkpt, "extensions")
            spd = ET.SubElement(ext, "speed")
            spd.text = str(speed)

    tree = ET.ElementTree(gpx)
    ET.indent(tree, "\t")
    tree.write(output_gpx, encoding="utf-8", xml_declaration=True)

    print(f"Saved {len(results)} GPS points to {output_gpx}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract GPS + speed from dashcam video to GPX"
    )
    parser.add_argument("video_path", help="Path to dashcam video file")
    parser.add_argument(
        "-o",
        "--output",
        help="Output GPX file, default: same name as video with .gpx",
        default=None,
    )
    parser.add_argument("-n", "--track-name", help="GPX track name", default=None)
    parser.add_argument(
        "-s",
        "--sample-seconds",
        type=int,
        help="Frame sampling interval in seconds, default: 5",
        default=5,
    )
    parser.add_argument(
        "-S",
        "--max-speed",
        type=int,
        help="Maximum speed (prevent false readings), default: 150",
        default=150,
    )

    args = parser.parse_args()

    if args.output is None:
        base, _ = os.path.splitext(args.video_path)
        args.output = base + ".gpx"

    if args.track_name is None:
        base, _ = os.path.splitext(args.video_path)
        args.track_name = "Route extracted from " + base

    extract_gps_from_video(
        args.video_path,
        args.output,
        args.track_name,
        sample_seconds=args.sample_seconds,
        max_speed=args.max_speed,
    )
