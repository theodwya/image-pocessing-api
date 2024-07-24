"""
Mock nvJPEG2000 Library

This mock library simulates the behavior of the actual nvJPEG2000 library
for local development without requiring a GPU.
"""

class nvjpeg2kHandle:
    pass

class nvjpeg2kDecodeState:
    pass

class nvjpeg2kEncodeState:
    pass

class nvjpeg2kStream:
    pass

def nvjpeg2kCreate():
    return nvjpeg2kHandle()

def nvjpeg2kDecodeStateCreate(handle):
    return nvjpeg2kDecodeState()

def nvjpeg2kEncodeStateCreate(handle):
    return nvjpeg2kEncodeState()

def nvjpeg2kStreamCreate(handle):
    return nvjpeg2kStream()

def nvjpeg2kStreamParse(handle, stream, data, length):
    pass

def nvjpeg2kStreamGetImageInfo(stream):
    class ImageInfo:
        width = 1920
        height = 1080
        num_components = 3
    return ImageInfo()

def nvjpeg2kDecode(handle, decode_state, stream, width, height, num_components, gpu_id):
    return b"decoded_image_data"

def nvjpeg2kEncode(handle, encode_state, stream, gpu_id):
    return b"encoded_image_data"

def nvjpeg2kDecodeStateDestroy(decode_state):
    pass

def nvjpeg2kEncodeStateDestroy(encode_state):
    pass

def nvjpeg2kStreamDestroy(stream):
    pass

def nvjpeg2kDestroy(handle):
    pass
