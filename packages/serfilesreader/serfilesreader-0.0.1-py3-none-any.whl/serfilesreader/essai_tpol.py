from serfilesreader import Serfile
import numpy as np
 
#########tests purpose#########
import functools,time,cv2


def time_it(func):
    """Timestamp decorator for dedicated functions"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()                 
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        mlsec = repr(elapsed).split('.')[1][:3]
        readable = time.strftime("%H:%M:%S.{}".format(mlsec), time.gmtime(elapsed))
        print('Function "{}": {} sec'.format(func.__name__, readable))
        return result
    return wrapper

################################

def savePng(frame, filename):
        if not 'png' in filename.split('.')[-1].lower() : 
            filename+='.png'
        #On 16 bits, it possible to have somme issue. So theses lines transform 16bits in 8 bits.
        index_maximum = np.amax(frame)
        datas = 256/index_maximum*frame.astype(int)
        return cv2.imwrite(filename, datas), filename


@time_it
def sum_frames(serfile_, index_begin=0, index_end=None, normalized=False) : 
    """return sum of all frames in ser files between index_begin (defautl 0) and index_end (default lenght of serfile)"""
    lenght = serfile_.getLength()
    serfile_.setCurrentPosition(0)
    if index_end == None:
        index_end=lenght
    sum_of_frames = np.zeros(serfile_.getWidth()*serfile_.getHeight())
    sum_of_frames = np.reshape(sum_of_frames,(serfile_.getHeight(),serfile_.getWidth()))
    for i in range( index_begin, index_end):
        sum_of_frames+=serfile_.read()[0]
    if normalized : 
        return (65536*(sum_of_frames - np.min(sum_of_frames))/np.ptp(sum_of_frames)).astype('uint16')
    return sum_of_frames

def blackOrWhite(frame, treshold):
    """return a Black or White frame. Black under treshold, white either"""
    return np.where(frame>treshold, 65535, 0)

def locate_ray(frame):
    """argument : numpy array
    return : rectangle x_left, y_left, x_right, y_right that englobe a ray"""
    
    pass

def returnFrameROI(frame, x_l, y_l, x_r, y_r):
    """return a ROI (Region Of Interest) of a frame, i.e. a subrectangle."""
    return frame[y_l:y_r+1, x_l:x_r+1]


monfichier = Serfile('Sun_104633.ser')
#print(sum_frames(monfichier,0,3500))
image_norm = sum_frames(monfichier,800,3200,True)
savePng(image_norm, 'test_outil.png')
savePng(returnFrameROI(image_norm,0,101,87,800), 'test_outil_ROI.png')
savePng(blackOrWhite(returnFrameROI(image_norm,0,101,87,800),32000), 'test_outil_ROI_Binarize.png')
