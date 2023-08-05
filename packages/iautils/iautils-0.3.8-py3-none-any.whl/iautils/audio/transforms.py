########################################################################################################################################
# AUDIO!!!
# iautils.audio.transforms
########################################################################################################################################
import numpy as np
import librosa, cv2
from scipy import signal
from functools import partial
import matplotlib.pyplot as plt
from .external import PyOctaveBand

from ..image.transforms import *


########################################################################################################################################
## RECIPES (Combination of Transformations)
########################################################################################################################################

################################################################
## RecipeGeneral
################################################################
class RecipeGeneral(object):
    '''
    소음 분석에 사용하는 일반적인 1D, 2D feature들을 계산함 - 자동 분석에 사용
    (현재) octave band pressure (1/3), rms, cog, sbw, flat, zcr, ose, stft, mel,
    '''
    
    def __init__(self, sr, specs=None):
        '''
        params
          sr
          specs
          steady <list or tuple>   range of steady [start_sec, end_sec]
        '''
        self.sr = sr
        self.specs = {'height': 224, 'hop_sec': 0.01, 'fft_sec': 0.08, 'unit': 'amplitude'} if specs is None else specs        
        
        self.hpf = BandPassFilter(sr)
        self.features = {
            # PCM
            'pcm': lambda y: y,
            # RMS
            'rms': RMS(sr, **{k: v for k, v in self.specs.items() if k in ['hop_sec', 'fft_sec', 'unit']}),
            # Center of Gravity
            'cog': SpectralCentroid(sr, **{k: v for k, v in self.specs.items() if k in ['hop_sec', 'fft_sec']}),
            # Spectral Bandwidth
            'sbw': SpectralBandwidth(sr, **{k: v for k, v in self.specs.items() if k in ['hop_sec', 'fft_sec']}),
            # Spectral Flatness
            'flat': SpectralFlatness(sr, **{k: v for k, v in self.specs.items() if k in ['hop_sec', 'fft_sec']}),
            # Zero Crossing Rate
            'zcr': ZeroCrossingRate(sr, **{k: v for k, v in self.specs.items() if k in ['hop_sec', 'fft_sec']}),
            # Onset Strength Envelope
            'ose': OnsetStrength(sr, **{k: v for k, v in self.specs.items() if k in ['height', 'hop_sec', 'fft_sec']}),
            # STFT
            'stft': STFT(sr, **self.specs),
            # Mel Spectrogram
            'mel': MelSpectrogram(sr, **self.specs),
            # Octave Band Sound Level (pressure)
            'obp': OctaveBandLevel(sr),
        }
        
    def __call__(self, y):
        y = self.hpf(y)
        features = {k: v(y) for k, v in self.features.items()}
        
        return features


################################################################
## RecipeMel
################################################################
class RecipeMel(object):
    '''
    1. Fixed hop length, 서로 다른 3개의 n_fft를 갖는 mel spectrograms을 구하여 image 형식 (heigth x width x 3 ch, 8 bit depth)의 array 생성
    2. image 형식의 array를 augment (image와 동일하게 처리) 
      (1) square crop (width만 crop하여 square image를 구함)
      (2) roll
      (3) flip
    
    return
      3d numpy array (height x width x channel)
    
    init. arguments
      height: default is 224 pixel (= number of frequency bins) to use ImageNet CNN models.
      hop_sec: default 0.01 sec (= 10 ms), hop_length = sampling rate * hop_sec
      n_fft_factors: n_fft_factor * hop_length = n_fft
    '''
    def __init__(self, sr, height=224, hop_sec=0.01, fft_secs=[0.08, 0.08, 0.08], augment=False):
        self.transoforms = []
        for fft_sec in fft_secs:
            self.transforms.append(MelSpectrogram(sr=sr, height=height, hop_sec=hop_sec, fft_sec=fft_sec))
        self.augment = augment
        
    def __call__(self, y):
        '''
        input
          y [numpy array], sr [int]
          
        return
          S [dB]
        '''
        # Stack Channels
        channels = []
        for t in self.transforms:
            S = t(y)
            S = ((S-S.min())/(S.max()-S.min()) * 255).astype(np.int)
            channels.append(S)
        x = np.stack(channels, -1)        
        
        # Augmentation
        if self.augment:
            x = SquareCrop('random')(x)
            x = Roll()(x)
            x = Flip()(x)
        else:
            x = SquareCrop('left')(x)
        
        return x

################################################################
## RecipeSTFT ~ multi layer
################################################################
class RecipeSTFT(object):
    '''
    1. 동일한 hop length와 서로 다른 3개의 n_fft를 갖는 STFT를 구하여 image 형식 (heigth x width x 3 ch, 8 bit depth)의 array 생성
    2. image 형식의 array를 augment (image와 동일하게 처리) 
      (1) square crop (width만 crop하여 square image를 구함)
      (2) roll
      (3) flip
    
    return 
      3d numpy array (height x width x channel).
    
    init. arguments
      height: default is 224 pixel (= number of frequency bins)
      hop_sec: default 0.01 sec (= 10 ms), hop_length = sampling rate * hop_sec
      n_fft_factors: n_fft_factor * hop_length = n_fft
    '''
    def __init__(self, sr, height=224, hop_sec=0.01, fft_secs=[0.08, 0.16, 0.32], augment=False):
        self.transforms = []
        for fft_sec in fft_secs:
            self.transforms.append(STFT(sr=sr, height=height, hop_sec=hop_sec, fft_sec=fft_sec))
        self.augment = augment
        
    def __call__(self, y, augment=False):
        '''
        input
          y [numpy array], sr [int]
          
        return
          S [dB]
        '''
        # Stack STFT spec.
        channels = []
        for t in self.transforms:
            S = t(y)
            S = ((S-S.min())/(S.max()-S.min()) * 255).astype(np.int)
            channels.append(S)
        x = np.stack(channels, -1)
        
        # Augmentation
        if self.augment:
            x = SquareCrop('random')(x)
            x = Roll()(x)
            x = Flip()(x)
        else:
            x = SquareCrop('left')(x)
        
        return x


##########################################################################################################################################
## FEATURE TRANSFORMS - FILTER, TEMPORAL, SPECTRAL, SPECTROGRAM, ...
##########################################################################################################################################
    
################################################################
## BandPassFilter (low-pass, band-pass, high-pass)
################################################################
class BandPassFilter(object):
    '''
    Bandpass filter이지만 cutoofs의 left가 None이면 lowpass, right가 None이면 highpass로 사용할 수 있음.
    
    init. Args:
      sr
      cutoffs
      order
    
    call Args:
      y
    
    Return:
      filtered y
    '''
    def __init__(self, sr=None, cutoffs=[12, None], order=5, ):
        
        # check cutoff
        for co in cutoffs:
            if (co is not None) and (sr is not None):
                if co > sr/2:
                    raise ValueError("[ERROR] cutoff frequency is higher than Nyquist limit.")
        
        # filter coefficient
        if (cutoffs[0] is not None) and (cutoffs[1] is None):
            sos = signal.butter(N=order, Wn=cutoffs[0], btype='highpass', fs=sr, output='sos')
        elif (cutoffs[0] is None) and (cutoffs[1] is not None):
            sos = signal.butter(N=order, Wn=cutoffs[1], btype='lowpass', fs=sr, output='sos')
        elif (cutoffs[0] is not None) and (cutoffs[1] is not None):
            sos = signal.butter(N=order, Wn=cutoffs, btype='bandpass', fs=sr, output='sos')
        else:
            raise ValueError("[ERROR] cutoffs required; cutoffs=[cultoff_left, cutoff_right]")
        
        self.sr = sr
        self.cutoffs = cutoffs
        self.order = order 
        self.sos = sos
        
    def __call__(self, y):
        
        return signal.sosfiltfilt(self.sos, y)


################################################################
# estimate changepoints - TRANSFORM 용도가 아님!!!
################################################################
def estimate_changepoints(X, use_diff=True, verbose=False):
    '''
    Args
      X          array (n x x) - pcm을 통째로 넣으면 터짐, rms 등으로 줄여서 넣어야 함
      use_diff   np.diff 후 changepoint 추정 (default)
    return
      bkpts <list>, states <np.array>, steady <int>
    '''
    
    # model & search range
    model = rpt.Pelt(model='rbf', jump=10)
    pens = range(1, 50)
    
    # use_diff
    X_ = np.pad(np.diff(X), ((0,0),(0,1)), 'edge') if use_diff else X

    # 빈도 가장 높은 no. of breaks를 선택
    l, n, n_max = 0, 0, 0
    bkpts = [X_.shape[1]]
    for pen in pens:
        b = model.fit_predict(X_.T, pen, )
        l_b = len(b)
        
        if l_b < 2:
            break
        elif l_b == l:
            n += 1
            if n > n_max:
                bkpts = b
                n_max = n
        else:
            n = 1
            l = l_b

    bkpt_prev = 0
    states = []
    for lab, bkpt in enumerate(bkpts):
        states += [lab] * (bkpt - bkpt_prev)
        bkpt_prev = bkpt
        
    # to np.array
    states = np.array(states, dtype=np.int)
    
    # estimate steady
    std_min = np.Inf
    for s in sorted(set(states)):
        std = X[:, states==s].std()
        if std < std_min:
            steady = s
            std_min = std
    
    if verbose:
        print(f"Check Changepoints:")
        print(f"  - {len(bkpts)} sections estimated, 0-{'-'.join([f'(section {str(i)})-{str(x)}' for i, x in enumerate(bkpts)])}")
        
    # last bkpt will be ignored - 닫힌 구간 표시용임
    return bkpts, states, steady


################################################################
## [SPECTRAL] Octave Band Sound Level
################################################################
class OctaveBandLevel(object):
    '''
    Octave band filter
    
    init. Args:
      sr
      fraction   bandwidth 'b', 1/3-octave b=3, 2/3-octave b=3/2, 1-octave b=1 (default 3)
      order
      limits
    
    call Args:
      y
      sr
    
    Return:
      spl
    '''
    def __init__(self, sr, fraction=3, order=6, fmin=12, fmax=12800, unit='dB'):
        
        self.sr = sr
        self.fraction = fraction
        self.order = order
        self.fmin = fmin
        self.fmax = fmax
        self.unit = unit.lower()
        
        # generate frequencies & remove outer frequency
        freq_arr = PyOctaveBand.getansifrequencies(self.fraction, self.fmin, self.fmax)
        idx = np.where(freq_arr[:, 2] > self.sr / 2)
        if any(idx[0]):
            freq_arr = np.delete(freq_arr, idx, axis=0)
        self.freqs = freq_arr[:, 0]
        self.freq_limits = freq_arr[:, 1:]
        self.N = self.freqs.shape[0]
        
        # Calculate the downsampling factor (array of integers with size [freq])   
        guard = 0.10
        factor = np.floor((self.sr / (2 + guard)) / self.freq_limits[:, 1])
        factor = np.clip(factor, 1, 50).astype('int')
        self.factor = factor
        
        # Get SOS filter coefficients (3d array w/ shape (freq, order, 6))
        butter = partial(signal.butter, self.order, btype='bandpass', output='sos')
        wns = self.freq_limits / (self.sr / self.factor /2).reshape(-1, 1)
        sos = np.apply_along_axis(butter, 1, wns)
        self.sos = sos
        
        # unit
        if self.unit in ['db']:
            self.unit_convert = lambda x: 20 * np.log10(x)
        elif self.unit in ['amp', 'amplitude']:
            self.unit_convert = lambda x: x
        elif self.unit in ['power']:
            self.unit_convert = lambda x: x**2
        
    def __call__(self, x):
        
        spl = np.zeros(self.N)    
        for idx in range(self.N):
            y = signal.decimate(x, self.factor[idx])
            y = signal.sosfilt(self.sos[idx], y)
            y = np.std(y) / 2e-5
            spl[idx] = self.unit_convert(y)
        
        return spl

    
################################################################
## FFT filter (arithmetic filter)
################################################################
# class FFT(object):
#     '''
    
#     '''
#      def __init__(self, sr=None, freq_width=60, harmonic_only=False):
        
#         if not sr:
#             self.sr = None
#             self.sr_ = 
#             self.freq_width = freq_width
#             self.harmonic_only = harmonic_only
        
#         else:         
#             # estimate sr if sr not specified
#             self.sr = sr if sr else fmax * 2
#             self.fraction = fraction
#             self.order = order
#             self.fmin = fmin
#             self.fmax = fmax

#             # generate frequencies & remove outer frequency
#             freq_arr = PyOctaveBand.getansifrequencies(self.fraction, self.fmin, self.fmax)
#             idx = np.where(freq_arr[:, 2] > self.sr / 2)
#             if any(idx[0]):
#                 freq_arr = np.delete(freq_arr, idx, axis=0)
#             self.freqs = freq_arr[:, 0]
#             self.freq_limits = freq_arr[:, 1:]
#             self.N = self.freqs.shape[0]

#             # Calculate the downsampling factor (array of integers with size [freq])   
#             guard = 0.10
#             factor = np.floor((self.sr / (2 + guard)) / self.freq_limits[:, 1])
#             factor = np.clip(factor, 1, 50).astype('int')
#             self.factor = factor

#             # Get SOS filter coefficients (3d array w/ shape (freq, order, 6))
#             butter = partial(signal.butter, self.order, btype='bandpass', output='sos')
#             wns = self.freq_limits / (self.sr / self.factor /2).reshape(-1, 1)
#             sos = np.apply_along_axis(butter, 1, wns)
#             self.sos = sos
        
#     def __call__(self, x, sr):
        
#         if sr != self.sr:
#             print(f"WARNING: sr ({sr}) is not equal to current sr ({self.sr}), sr updated.")
#             self.__init__(sr, self.fraction, self.order, self.fmin, self.fmax)
            
#         spl = np.zeros(self.N)
            
#         for idx in range(self.N):
#             y = signal.decimate(x, self.factor[idx])
#             y = signal.sosfilt(self.sos[idx], y)
#             y = np.std(y)
#             spl[idx] = 20 * np.log10(y / 2e-5)
        
#         return spl


################################################################
## [TIME-DOMAIN] RMS
################################################################
class RMS(object):
    '''
    root mean squared spl along time axis - 각 time bin에서 energy의 RMS
    '''
    def __init__(self, sr, hop_sec=0.01, fft_sec=0.08, center=True, unit='amplitude'):
                
        self.sr = sr
        self.hop_sec = hop_sec
        self.fft_sec = fft_sec
        self.center = center
        self.unit = unit.lower()
        
        self.frame_length = int(self.sr * self.fft_sec)
        self.hop_length = int(self.sr * self.hop_sec)
        
        if self.unit in ['db']:
            self.unit_convert = lambda x: 20 * np.log10(x)
        elif self.unit in ['amp', 'amplitude']:
            self.unit_convert = lambda x: x
        elif self.unit in ['power']:
            self.unit_convert = lambda x: x**2
        
    def __call__(self, y):
        
        rms = librosa.feature.rms(y, frame_length=self.frame_length, hop_length=self.hop_length, center=self.center)
        if y.ndim == 1:
            rms = rms[0]
        rms = self.unit_convert(rms)
        
        return rms
    
    
################################################################
## [TIME-DOMAIN] SpectralCentroid (Center of Gravity)
################################################################
class SpectralCentroid(object):
    '''
    spectral centroid along time axis - 각 time bin에서 frequency의 center
    '''
    def __init__(self, sr, hop_sec=0.01, fft_sec=0.08, center=True):
                
        self.sr = sr
        self.hop_sec = hop_sec
        self.fft_sec = fft_sec
        self.center = center
        
        self.n_fft = int(self.sr * self.fft_sec)
        self.hop_length = int(self.sr * self.hop_sec)
        
    def __call__(self, y):
                    
        cog = librosa.feature.spectral_centroid(y, self.sr, n_fft=self.n_fft, hop_length=self.hop_length, center=self.center)
        if y.ndim == 1:
            cog = cog[0]
        
        return cog
    
    
################################################################
## [TIME-DOMAIN] SpectralBandwidth
################################################################
class SpectralBandwidth(object):
    '''
    spectral bandwidth along time axis - 각 time bin에서 frequency의 bandwidth
    '''
    def __init__(self, sr, hop_sec=0.01, fft_sec=0.08, p=2, center=True):
        
        self.sr = sr
        self.hop_sec = hop_sec
        self.fft_sec = fft_sec
        self.p = p
        self.center = center
        
        self.n_fft = int(self.sr * self.fft_sec)
        self.hop_length = int(self.sr * self.hop_sec)
        
    def __call__(self, y):
            
        sbw = librosa.feature.spectral_bandwidth(y, self.sr, n_fft=self.n_fft, hop_length=self.hop_length, center=self.center, p=self.p)
        if y.ndim == 1:
            sbw = sbw[0]
        
        return sbw
     
    
################################################################
## [TEMPORAL] SpectralFlatness
################################################################
class SpectralFlatness(object):
    '''
    spectral flatness along time axis - 각 time bin에서 frequency의 bandwidth
    '''
    def __init__(self, sr, hop_sec=0.01, fft_sec=0.08, center=True, unit='amplitude'):
        
        self.sr = sr
        self.hop_sec = hop_sec
        self.fft_sec = fft_sec
        self.center = center
        self.unit = unit
        
        self.n_fft = int(self.sr * self.fft_sec)
        self.hop_length = int(self.sr * self.hop_sec)
        
        if self.unit in ['db']:
            self.power = 1
            self.unit_convert = lambda x: 20 * np.log10(x)
        elif self.unit in ['amp', 'amplitude']:
            self.power = 1
            self.unit_convert = lambda x: x
        elif self.unit in ['power']:
            self.power = 2
            self.unit_convert = lambda x: x
        
    def __call__(self, y):
            
        flat = librosa.feature.spectral_flatness(y, n_fft=self.n_fft, hop_length=self.hop_length, center=self.center, power=self.power)
        if y.ndim == 1:
            flat = flat[0]
        flat = self.unit_convert(flat)
        
        return flat
    
    
################################################################
## [TEMPORAL] ZeroCrossingRate
################################################################
class ZeroCrossingRate(object):
    '''
    root mean squared spl along time axis - 각 time bin에서 energy의 RMS
    '''
    def __init__(self, sr, hop_sec=0.01, fft_sec=0.08, center=True):
        
        self.sr = sr
        self.hop_sec = hop_sec
        self.fft_sec = fft_sec
        self.center = center
        
        self.frame_length = int(self.sr * self.fft_sec)
        self.hop_length = int(self.sr * self.hop_sec)
        
    def __call__(self, y):

        zcr = librosa.feature.zero_crossing_rate(y, frame_length=self.frame_length, hop_length=self.hop_length, center=self.center)
        if y.ndim == 1:
            zcr = zcr[0]
        
        return zcr
        
    
################################################################
## [Onset] OnsetStrength
################################################################
class OnsetStrength(object):
    '''
    onset strength
    (fixed) mel feature, power=1.0 
    '''
    def __init__(self, sr, height=224, hop_sec=0.01, fft_sec=0.08, fmin=0, fmax=None, center=True):
        
        # type
        self._type_ = 'audio'
        
        self.sr = sr
        self.height = height
        self.hop_sec = hop_sec
        self.fft_sec = fft_sec
        self.center = center
        self.fmin = fmin
        fmax = fmax if fmax is not None else int(sr/2)
        self.fmax = fmax
        
        self.n_fft = int(self.sr * self.fft_sec)
        self.hop_length = int(self.sr * self.hop_sec)
        
    def __call__(self, y):
            
        ose = librosa.onset.onset_strength(
            y, self.sr, n_fft=self.n_fft, hop_length=self.hop_length, n_mels=self.height, fmin=self.fmin, fmax=self.fmax, center=self.center, 
        )
        
        return ose

    
################################################################
## Mel Spectrogram
################################################################
class MelSpectrogram(object):
    '''
    librosa.feature.melspectrogram을 height, hop_sec에 대해 다시 작성한 것.
    
    init. Args:
      height: default is 224 pixel (= number of frequency bins)
      hop_sec: default 0.01 sec (= 10 ms), hop_length = sampling rate * hop_sec    
    
    return 
      2d numpy array, unit dB
    '''
    def __init__(self, sr, height=224, hop_sec=0.01, fft_sec=0.08, fmin=0, fmax=None, center=True, unit='dB'):
                
        self.sr = sr
        self.height = height
        self.hop_sec = hop_sec
        self.fft_sec = fft_sec
        self.fmin = fmin
        self.fmax = fmax if fmax is not None else int(sr/2)
        self.center = True
        
        # calcs
        self.hop_length = int(self.sr * self.hop_sec)
        self.n_fft = int(self.sr * self.fft_sec)
        self.freqs = librosa.mel_frequencies(n_mels=self.height, fmin=self.fmin, fmax=self.fmax)
        
        if unit.lower() in ['db']:
            self.power = 2
            # self.unit_convert = librosa.power_to_db
            self.unit_convert = lambda x: 10 * np.log10(x)
        elif unit.lower() in ['amp', 'amplitude']:
            self.power = 1
            self.unit_convert = lambda x: x
        elif unit.lower() in ['power']:
            self.power = 2
            self.unit_convert = lambda x: x
            
        # placeholder
        self.S = None
        
    def __call__(self, y):
        
        # get mel
        S = librosa.feature.melspectrogram(
            y, self.sr, 
            n_fft=self.n_fft, 
            hop_length=self.hop_length, 
            n_mels=self.height, 
            fmin=self.fmin, 
            fmax=self.fmax, 
            center=self.center, 
            power=self.power
        )
        
        # unit convert
        S = self.unit_convert(S)
        
        # update S
        self.S = S
        
        return S
    
    def show(self, savepath=None, H=None, dpi=72, ticks=False):
        if self.S is None:
            return
        
        S = self.S
        
        if H is None:
            H = S.shape[0] / dpi
            
        W = H / S.shape[0] * S.shape[1]
        
        # plot
        fig, ax = plt.subplots(figsize=(W, H))
        ax.imshow(S, origin='lower', cmap='magma', )
        
        # ticks
        if ticks:    
            plt.xticks(
                [i for i in np.arange(0, S.shape[1]+1) if i % int(1/self.hop_sec) == 0], 
                [int(i*self.hop_sec) for i in np.arange(0, S.shape[1]+1) if i % int(1/self.hop_sec) == 0], 
            )
            plt.yticks(
                [i for i, e in enumerate(self.freqs) if i % int(S.shape[0]/10) == 0], 
                [np.int(e) for i, e in enumerate(self.freqs) if i % int(S.shape[0]/10) == 0], 
            )
        else:
            ax.set_axis_off()
        
        # save
        if savepath is not None:
            plt.savefig(savepath, dpi=dpi)
        else:
            plt.show()

    
################################################################
## STFT
################################################################
class STFT(object):
    '''
    librosa.STFT를 height, hop_sec에 대해 다시 작성한 것.
    계산 중 sr이 변경되면 self.sr re-initiate됨.
    height는 cv2로 resize되고, height=None이면 resize 없이 n_fft에 따라 height 결정됨
    
    return 
      2d numpy array, unit dB
    
    init. arguments
      height: default is 224 pixel (= number of frequency bins)
      hop_sec: default 0.01 sec (= 10 ms), hop_length = sampling rate * hop_sec
      
    example
      get_stft = STFT()
      S = get_stft(y, sr)
    '''
    def __init__(self, sr, height=224, hop_sec=0.01, fft_sec=None, center=True, unit='dB'):
        
        self.sr = sr
        self.height = height
        self.hop_sec = hop_sec
        self.fft_sec = fft_sec if fft_sec is not None else hop_sec * 8
        self.center = center
        self.unit = unit.lower()
        
        # calcs
        self.hop_length = int(self.sr * self.hop_sec)
        self.n_fft = int(self.sr * self.fft_sec)
        self.freqs = librosa.fft_frequencies(self.sr, self.n_fft)
        
        if self.unit in ['db']:
            self.unit_convert = lambda x: 20 * np.log10(np.abs(x))
        elif self.unit in ['amp', 'amplitude']:
            self.unit_convert = lambda x: np.abs(x)
        elif self.unit in ['power']:
            self.unit_convert = lambda x: np.abs(x) ** 2
        elif self.unit in ['complex']:
            self.unit_convert = lambda x: x
            if self.height is not None:
                print('WARNING!!! if unit is complex, resize cannot be done. height is changed to None.')
        else:
            print('WARNING!!! wrong unit, it will return dB')
            self.unit_convert = lambda x: librosa.amplitude_to_db(np.abs(x))
        
        # avoid cv2 freeze issue
        cv2.setNumThreads(0)
        
    def __call__(self, y):
        
        # get stft
        S = librosa.stft(
            y, 
            n_fft=self.n_fft, 
            hop_length=self.hop_length,
            center=self.center,
        )
            
        # unit convert
        S = self.unit_convert(S)
        
        # resize
        if self.height is not None:
            S = cv2.resize(S, (S.shape[1], self.height))
        
        return S
    
    def show(self, savepath=None, H=None, dpi=72, ticks=False):
        if self.S is None:
            return
        
        S = self.S
        
        if H is None:
            H = S.shape[0] / dpi
            
        W = H / S.shape[0] * S.shape[1]
        
        # plot
        fig, ax = plt.subplots(figsize=(W, H))
        ax.imshow(S, origin='lower', cmap='magma', )
        
        # ticks
        if ticks:    
            plt.xticks(
                [i for i in np.arange(0, S.shape[1]+1) if i % int(1/self.hop_sec) == 0], 
                [int(i*self.hop_sec) for i in np.arange(0, S.shape[1]+1) if i % int(1/self.hop_sec) == 0], 
            )
            plt.yticks(
                [i for i, e in enumerate(self.freqs) if i % int(S.shape[0]/10) == 0], 
                [np.int(e) for i, e in enumerate(self.freqs) if i % int(S.shape[0]/10) == 0], 
            )
        else:
            ax.set_axis_off()
        
        # save
        if savepath is not None:
            plt.savefig(savepath, dpi=dpi)
        else:
            plt.show()
  
    
    
  ################################################################
  ## DWT
  ################################################################



  ################################################################
  ## CWT
  ################################################################



################################################################
## Scale
################################################################
# 0 ~ 1 float
# 0 ~ 255 uint8
# class FreqStandardization(object):
#     '''
#     Frequency Standardization (Mean, std are required)
    
#     init arguments
#       mean, std
      
#     return
#       input
#     '''
#     def __init__(self, mean=None, std=None, cutoff=(-3, 3)):
        
#         self.mean = mean
#         self.std = std
#         self.cutoff = cutoff
        
#     def __call__(self, y, sr):
#         '''
#         input
#           y [numpy array], sr [int]
          
#         return
#           S [dB]
#         '''
#         if all([x is not None for x in [self.mean, self.std]]):
#             y = (y - self.mean) / self.std
#             cutL, cutH = self.cutoff
#             y = np.clip(y, cutL, cutH)
#             y = (y - cutL) / (cutH - cutL) 
#         else:
#             print("mean, std are required!")
#         return y, sr
