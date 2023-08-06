def sum_frames(serfile, index_begin=0, index_end=None) : 
    """return sum of all frames in ser files between index_begin (defautl 0) and index_end (default lenght of serfile)"""
    lenght = serfile.getLength()
    if index_end = None
        index_end=lenght
    sum_of_frames = np.array([])
    for i in range( index_begin, index_end):
        sum_of_frames+=serfile.read()[0]
    return sum_of_frames

def locate_ray(frame):
    """argument : numpy array
    return : rectangle x_left, y_left, x_right, y_right that englobe a ray"""
