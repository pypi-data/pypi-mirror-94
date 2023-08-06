
def encode_rle():
    pass

def decode_rle():
    pass




import numpy as np # linear algebra

def rleToMask(rleString, height, width):
    """
    This function is an rle to mask converter.
    You supply the rle string for one mask, along with it's height and width
    from the solutions for stage1 and it will return the mask.

    Source: https://www.kaggle.com/robertkag/rle-to-mask-converter
    """

    rows, cols = height,width
    rleNumbers = [int(numstring) for numstring in rleString.split(' ')]
    rlePairs = np.array(rleNumbers).reshape(-1,2)
    img = np.zeros(rows*cols,dtype=np.uint8)
    for index,length in rlePairs:
    index -= 1
    img[index:index+length] = 255
    img = img.reshape(cols,rows)
    img = img.T
    return img


def rle_decoding(rle_arr, w, h):
    indices = []
    for idx, cnt in zip(rle_arr[0::2], rle_arr[1::2]):
        indices.extend(list(range(idx-1, idx+cnt-1)))  # RLE is 1-based index
    mask = np.zeros(h*w, dtype=np.uint8)
    mask[indices] = 1
    return mask.reshape((w, h)).T