from typing import Iterable

import cv2

from .common import Frame, FrameGroup


def flat_frames(wrapped_cap) -> Iterable[Frame]:
    for frame_group in wrapped_cap:
        for frame in frame_group.frames:
            yield frame


def cap_wrapper(cap, detector_fps=-1):
    cap_fps = cap.get(cv2.CAP_PROP_FPS)

    target_time_between_frames = 0
    if detector_fps != -1:
        target_time_between_frames = 1 / detector_fps

    prev_frame_time = None

    frame_group = []
    while True:
        ret, image = cap.read()

        if not ret:
            return

        fr_idx = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        fr_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        frame_group.append(Frame(image, fr_idx, fr_time))

        if prev_frame_time is not None and fr_time - prev_frame_time < target_time_between_frames:
            continue

        prev_frame_time = fr_time
        yield FrameGroup(frame_group)
        frame_group = []
