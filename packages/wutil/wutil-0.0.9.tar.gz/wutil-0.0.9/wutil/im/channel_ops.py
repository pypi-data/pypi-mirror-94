def is_channel_first(im):
    return im.shape[0] in (1, 3, 4)

def is_channel_last(im):
    return im.shape[-1] in (1, 3, 4)

def to_channel_first(im):
    if not is_channel_first(im):
        return im.transpose([2, 0, 1])
    return im

def to_channel_last(im):
    if not is_channel_last(im):
        return im.transpose([1, 2, 0])
    return im
