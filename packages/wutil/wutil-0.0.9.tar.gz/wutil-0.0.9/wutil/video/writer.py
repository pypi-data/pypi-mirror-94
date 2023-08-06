import cv2


def video_writer(out_p: str, fps: float, vid_width: int, vid_height: int) -> cv2.VideoWriter:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    return cv2.VideoWriter(out_p, fourcc, fps, (vid_width, vid_height))


def video_writer_from_cap(cap: cv2.VideoCapture, out_p: str) -> cv2.VideoWriter:
    fps = cap.get(cv2.CAP_PROP_FPS)

    vid_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vid_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    return video_writer(out_p, fps, vid_width, vid_height)
