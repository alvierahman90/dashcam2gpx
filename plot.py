import gpxpy

import matplotlib.pyplot as plt

def extract_speeds_from_gpx(gpx_file):
    with open(gpx_file, 'r') as f:
        gpx = gpxpy.parse(f)
    speeds = []
    times = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point_idx in range(1, len(segment.points)):
                prev_point = segment.points[point_idx - 1]
                curr_point = segment.points[point_idx]
                time_diff = (curr_point.time - prev_point.time).total_seconds()
                if time_diff > 0:
                    dist = curr_point.distance_3d(prev_point)
                    speed = dist / time_diff * 3.6
                    speeds.append(speed)
                    times.append(curr_point.time)
    return times, speeds

if __name__ == "__main__":
    gpx_file = "tests/output.gpx"
    times, speeds = extract_speeds_from_gpx(gpx_file)
    plt.plot(times, speeds)
    plt.xlabel("Time")
    plt.ylabel("Speed (km/h)")
    plt.title("Speed over Time from GPX")
    plt.show()