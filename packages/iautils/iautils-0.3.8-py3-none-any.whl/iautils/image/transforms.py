########################################################################################################################################
# Image!!!
# iautils.image.transforms
########################################################################################################################################
import numpy as np
import cv2
from albumentations.core.transforms_interface import BasicTransform, ImageOnlyTransform
from albumentations.core.composition import Compose as ABCompose
from albumentations.augmentations.transforms import *

__all__ = [
    # defined here
    "Compose",
    "ToImage",
    "SquareCrop",
    "Resize",
    "Roll",
    # from Albumentations
    "ABCompose",
    "Blur",
    "VerticalFlip",
    "HorizontalFlip",
    "Flip",
    "Normalize",
    "Transpose",
    "RandomGamma",
    "OpticalDistortion",
    "GridDistortion",
    "RandomGridShuffle",
    "HueSaturationValue",
    "PadIfNeeded",
    "RGBShift",
    "RandomBrightness",
    "RandomContrast",
    "MotionBlur",
    "MedianBlur",
    "GaussianBlur",
    "GaussNoise",
    "GlassBlur",
    "CLAHE",
    "ChannelShuffle",
    "InvertImg",
    "ToGray",
    "ToSepia",
    "JpegCompression",
    "ImageCompression",
    "Cutout",
    "CoarseDropout",
    "ToFloat",
    "FromFloat",
    "RandomBrightnessContrast",
    "RandomSnow",
    "RandomRain",
    "RandomFog",
    "RandomSunFlare",
    "RandomShadow",
    "Lambda",
    "ChannelDropout",
    "ISONoise",
    "Solarize",
    "Equalize",
    "Posterize",
    "Downscale",
    "MultiplicativeNoise",
    "FancyPCA",
    "MaskDropout",
    "GridDropout",
    "ColorJitter",
]

########################################################################################################################################
## COMPOSE
########################################################################################################################################
class Compose(object):
    """
    Args:
      transforms (list of ``Transform`` objects): list of transforms to compose.

    Example:
      >>> transforms.Compose([
      >>>     transforms.CenterCrop(10),
      >>>     transforms.ToTensor(),
      >>> ])
    """

    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, y):
        for t in self.transforms:
            if isinstance(t, BasicTransform):
                y = t(image=y)['image']
            else:
                y = t(y)
        return y

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        for t in self.transforms:
            format_string += '\n'
            format_string += '    {0}'.format(t)
        format_string += '\n)'
        return format_string
    
    
########################################################################################################################################
## IMAGE TRANSFORMATION (Crop, Flip, Rolling, ...)
########################################################################################################################################

################################################################
## ToImage
################################################################
class ToImage(ImageOnlyTransform):
    '''
    shape (H, W) numpy to shape (H, W, 3) w/ dtype uint8 numpy
    (NOTE) 전체 데이터로부터 추정된 x_min, x_max를 사용한 Normalize가 가장 권장 됨
    
    Methods:
      0   Normalize
      1   Standardize along y-axis
    
    Args:
      method         
      x_min, x_max   (for Normalize) use each image's min, max if None
      x_mean, x_std  (for Standardize) use each image's mean, std if None
      z_min, z_max   (for Stardardize) default -2, +2 ~ clip standardize result
      cmap           color map (gray to color) ['magma', 'bone', 'jet', 'winter', ...] ~ see cv2's COLORMAP_*
    
    Returns:
      <np.ndarray> HWC, RGB
    '''
    
    def __init__(self, method=0, x_min=None, x_max=None, x_mean=None, x_std=None, z_min=-2, z_max=2, cmap=None):
        super(ToImage, self).__init__(always_apply=True, p=1.0)
        
        self.method = method
        self.x_min, self.x_max = x_min, x_max
        self.x_mean, self.x_std = x_mean, x_std
        self.z_min, self.z_max = z_min, z_max
        self.cmap = eval(f"cv2.COLORMAP_{cmap.upper()}") if cmap is not None else None
        
        # avoid cv2 freeze issue
        cv2.setNumThreads(0)
        
    def apply(self, image, **params):
        # Normalize
        x = self.convert(image)
        
        # (H x W) to (H x W x C) w/ uint8
        if x.ndim == 2:
            x = np.expand_dims(x, -1)
        x = np.uint8(x * 255)
        
        # Apply Colormap
        if self.cmap is not None:
            x = cv2.applyColorMap(x, self.cmap)
        x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)            
        
        return x

    def get_transform_init_args_names(self):
        return ("method", "x_min", "x_max", "x_mean", "x_std", "z_min", "z_max", "cmap")
    
    def convert(self, x):
        # do normalize
        if self.method in [0]:
            x_min = np.min(x) if self.x_min is None else self.x_min
            x_max = np.max(x) if self.x_max is None else self.x_max
            x = (x-x_min)/(x_max-x_min)
            
        # do standardize
        elif self.method in [1]:
            x_mean = np.mean(x) if self.x_mean is None else self.x_mean
            x_std = np.std(x) if self.x_std is None else self.x_std
            x = (x-x_mean)/x_std
            x = (x-self.z_min)/(self.z_max-self.z_min)            
            
        return x
    
    
################################################################
## Square Crop
################################################################
class SquareCrop(ImageOnlyTransform):   
    '''
    모든 변환은 Channel Last 기준 (h x w x c), pytorch에서 사용하려면 (c x h)
    (NOTE!) Spectrogram Crop 용으로 제작되어 height는 고정되고 width만 height와 동일하게 crop함
    
    Init
    ---------------
    position : string
      'left', 'center', 'right', 'random'
      
    Call
    ----
    sqaured cropped image : np.ndarray
    '''
    def __init__(self, position='random', always_apply=True, p=1.0):
        super(SquareCrop, self).__init__(always_apply, p)
        self.position = position
    
    def apply(self, image, **params):
        x = image
        
        if x.ndim == 2:
            x = np.expand_dims(x, -1)
        h, w, c = x.shape
            
        #### if width is smaller than height, drop the data 
        if w <= h:
            return x

        #### do crop
        if self.position == 'left':
            x = x[:, :h, :]
        elif self.position == 'center': 
            x = x[:, w//2-h//2:w//2+h//2, :]
        elif self.position == 'right':
            x = x[:, -h:, :]
        elif self.position == 'random':
            l = np.random.randint(0, w - h)
            x = x[:, l:l+h, :]
        else:
            print('ERROR!!! crop options: [left, center, right, random]')  
                
        return x

    def get_transform_init_args_names(self):
        return ("position")

    
################################################################
## Resize
################################################################
class Resize(ImageOnlyTransform):
    '''
    모든 변환은 Channel Last 기준 (HWC)
    
    Init.
    -----
    shape : tuple
    fixed_aspect : bool

    Call
    ----
    resized image : np.ndarray
    '''
    def __init__(self, shape=(224, 224), fixed_aspect=False, always_apply=True, p=1.0):
        super(Resize, self).__init__(always_apply, p)
        
        # 사용자 편의를 위해 - tuple이 아닌 single value가 들어오면 해당 값은 height로 간주
        if not isinstance(shape, tuple):
            shape = (shape, None)
        
        self.shape = shape
        self.height, self.width = shape
        self.fixed_aspect = fixed_aspect
        
    def apply(self, image, **params):
        x = image
        
        if x.ndim == 2:
            x = np.expand_dims(x, -1)
        h, w, c = x.shape
        
        # set resize width x height
        width, height = self.width, self.height
        if width is None:
            width = int(height * w/h) if self.fixed_aspect else w
        if height is None:
            height = int(width * h/w) if self.fixed_aspect else h
            
        # do resize
        x = cv2.resize(x, (width, height))
        
        return x
    
    def get_transform_init_args_names(self):
        return ("shape", "fixed_aspect")
    
    
################################################################
## Rolling
################################################################
class Roll(ImageOnlyTransform):
    '''
    모든 변환은 Channel Last 기준 (HWC)
    
    Init.
    -----
    shift : str or int
      'random', 또는 integer 입력되면 그 값의 pixel만큼 Roll
    direction : str
      'x' 또는 'y', Roll은 Spectrogram 용으로 작성하였기 때문에 default는 x (time-axis)
      
    Example
    -------
    >>> roll = Roll()
    >>> img_shifted = roll(img)
      
    Returns
    -------
    rolled image : np.ndarray
    '''
    def __init__(self, shift='random', direction='x', always_apply=False, p=0.5):
        super(Roll, self).__init__(always_apply, p)
        self.shift = shift
        self.direction = direction.lower()
        
        if self.direction not in ['x', 'y']:
            raise ValueError(f"Input direction not in ['x', 'y']!")
    
    def apply(self, image, **params):
        x = image
        
        if x.ndim == 2:
            x = np.expand_dims(x, -1)
            
        # roll    
        axis = 1 if self.direction in ['x'] else 0   # H: 0, W: 1, C: 2
        max_shift = x.shape[axis]

        # do roll
        if isinstance(self.shift, int):
            shift = self.shift
        elif self.shift == 'random':
            shift = np.random.randint(0, max_shift)
        else:
            shift = 0

        x = np.roll(x, shift, axis)
            
        return x
    
    def get_transform_init_args_names(self):
        return ("shift", "direction")
        
        
################################################################################################################################
# 아래 Albumentations의 Transforms들이 이 모듈에 로드되어 있음
################################################################################################################################
AVAILABLES = {
    'Blur': "Blur(always_apply=False, p=0.5, blur_limit=(3, 7))",
    'VerticalFlip': "VerticalFlip(always_apply=False, p=0.5)",
    'HorizontalFlip': "HorizontalFlip(always_apply=False, p=0.5)",
    'Flip': "Flip(always_apply=False, p=0.5)",
    'Normalize': "Normalize(always_apply=False, p=1.0, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0)",
    'Transpose': "Transpose(always_apply=False, p=0.5)",
    'RandomGamma': "RandomGamma(always_apply=False, p=0.5, gamma_limit=(80, 120), eps=None)",
    'OpticalDistortion': "OpticalDistortion(always_apply=False, p=0.5, distort_limit=(-0.05, 0.05), shift_limit=(-0.05, 0.05), interpolation=1, border_mode=4, value=None, mask_value=None)",
    'GridDistortion': "GridDistortion(always_apply=False, p=0.5, num_steps=5, distort_limit=(-0.3, 0.3), interpolation=1, border_mode=4, value=None, mask_value=None)",
    'RandomGridShuffle': "RandomGridShuffle(always_apply=False, p=0.5, grid=(3, 3))",
    'HueSaturationValue': "HueSaturationValue(always_apply=False, p=0.5, hue_shift_limit=(-20, 20), sat_shift_limit=(-30, 30), val_shift_limit=(-20, 20))",
    'PadIfNeeded': "PadIfNeeded(always_apply=False, p=1.0, min_height=1024, min_width=1024, pad_height_divisor=None, pad_width_divisor=None, border_mode=4, value=None, mask_value=None)",
    'RGBShift': "RGBShift(always_apply=False, p=0.5, r_shift_limit=(-20, 20), g_shift_limit=(-20, 20), b_shift_limit=(-20, 20))",
    'RandomBrightness': "RandomBrightness(always_apply=False, p=0.5, limit=(-0.2, 0.2))",
    'RandomContrast': "RandomContrast(always_apply=False, p=0.5, limit=(-0.2, 0.2))",
    'MotionBlur': "MotionBlur(always_apply=False, p=0.5, blur_limit=(3, 7))",
    'MedianBlur': "MedianBlur(always_apply=False, p=0.5, blur_limit=(3, 7))",
    'GaussianBlur': "GaussianBlur(always_apply=False, p=0.5, blur_limit=(3, 7), sigma_limit=(0, 0))",
    'GaussNoise': "GaussNoise(always_apply=False, p=0.5, var_limit=(10.0, 50.0))",
    'GlassBlur': "GlassBlur(always_apply=False, p=0.5, sigma=0.7, max_delta=4, iterations=2)",
    'CLAHE': "CLAHE(always_apply=False, p=0.5, clip_limit=(1, 4.0), tile_grid_size=(8, 8))",
    'ChannelShuffle': "ChannelShuffle(always_apply=False, p=0.5)",
    'InvertImg': "InvertImg(always_apply=False, p=0.5)",
    'ToGray': "ToGray(always_apply=False, p=0.5)",
    'ToSepia': "ToSepia(always_apply=False, p=0.5)",
    'JpegCompression': "JpegCompression(always_apply=False, p=0.5, quality_lower=99, quality_upper=100)",
    'ImageCompression': "ImageCompression(always_apply=False, p=0.5, quality_lower=99, quality_upper=100, compression_type=0)",
    'Cutout': "Cutout(always_apply=False, p=0.5, num_holes=8, max_h_size=8, max_w_size=8)",
    'CoarseDropout': "CoarseDropout(always_apply=False, p=0.5, max_holes=8, max_height=8, max_width=8, min_holes=8, min_height=8, min_width=8, fill_value=0, mask_fill_value=None)",
    'ToFloat': "ToFloat(always_apply=False, p=1.0, max_value=None)",
    'FromFloat': "FromFloat(always_apply=False, p=1.0, dtype='uint16', max_value=None)",
    'RandomBrightnessContrast': "RandomBrightnessContrast(always_apply=False, p=0.5, brightness_limit=(-0.2, 0.2), contrast_limit=(-0.2, 0.2), brightness_by_max=True)",
    'RandomSnow': "RandomSnow(always_apply=False, p=0.5, snow_point_lower=0.1, snow_point_upper=0.3, brightness_coeff=2.5)",
    'RandomRain': "RandomRain(always_apply=False, p=0.5, slant_lower=-10, slant_upper=10, drop_length=20, drop_width=1, drop_color=(200, 200, 200), blur_value=7, brightness_coefficient=0.7, rain_type=None)",
    'RandomFog': "RandomFog(always_apply=False, p=0.5, fog_coef_lower=0.3, fog_coef_upper=1, alpha_coef=0.08)",
    'RandomSunFlare': "RandomSunFlare(always_apply=False, p=0.5, flare_roi=(0, 0, 1, 0.5), angle_lower=0, angle_upper=1, num_flare_circles_lower=6, num_flare_circles_upper=10, src_radius=400, src_color=(255, 255, 255))",
    'RandomShadow': "RandomShadow(always_apply=False, p=0.5, shadow_roi=(0, 0.5, 1, 1), num_shadows_lower=1, num_shadows_upper=2, shadow_dimension=5)",
    'Lambda': "Lambda(name=None, image=<function noop at 0x7f402a0763a0>, mask=<function noop at 0x7f402a0763a0>, keypoint=<function noop at 0x7f402a0763a0>, bbox=<function noop at 0x7f402a0763a0>, always_apply=False, p=1.0)",
    'ChannelDropout': "ChannelDropout(always_apply=False, p=0.5, channel_drop_range=(1, 1), fill_value=0)",
    'ISONoise': "ISONoise(always_apply=False, p=0.5, intensity=(0.1, 0.5), color_shift=(0.01, 0.05))",
    'Solarize': "Solarize(always_apply=False, p=0.5, threshold=(128, 128))",
    'Equalize': "Equalize(always_apply=False, p=0.5, mode='cv', by_channels=True)",
    'Posterize': "Posterize(always_apply=False, p=0.5, num_bits=(4, 4))",
    'Downscale': "Downscale(always_apply=False, p=0.5, scale_min=0.25, scale_max=0.25, interpolation=0)",
    'MultiplicativeNoise': "MultiplicativeNoise(always_apply=False, p=0.5, multiplier=(0.9, 1.1), per_channel=False, elementwise=False)",
    'FancyPCA': "FancyPCA(always_apply=False, p=0.5, alpha=0.1)",
    'MaskDropout': "MaskDropout(always_apply=False, p=0.5, max_objects=(1, 1), image_fill_value=0, mask_fill_value=0)",
    'GridDropout': "GridDropout(always_apply=False, p=0.5, ratio=0.5, unit_size_min=None, unit_size_max=None, holes_number_x=None, holes_number_y=None, shift_x=0, shift_y=0, mask_fill_value=None, random_offset=False)",
    'ColorJitter': "ColorJitter(always_apply=False, p=0.5, brightness=[0.8, 1.2], contrast=[0.8, 1.2], saturation=[0.8, 1.2], hue=[-0.2, 0.2])",
}
