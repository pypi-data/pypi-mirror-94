from dataclasses import dataclass
import numpy as np


@dataclass
class Frame(object):
    data: np.array
    idx: int
    time: float

@dataclass
class FrameGroup(object):
    frames: [Frame]

    @property
    def last_frame(self):
        return self.frames[-1]

    def __len__(self):
        return len(self.frames)