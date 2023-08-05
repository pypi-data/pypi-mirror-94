########################################################################################################################################
# AUDIO!!!
# iautils.audio.transforms
########################################################################################################################################
import numpy as np
import ruptures as rpt


########################################################################################################################################
## CHANGEPOINT
########################################################################################################################################

################################################################
# estimate changepoints - TRANSFORM 용도가 아님!!!
################################################################
def estimate_changepoints(X, use_diff=True, pelt_model='rbf', pens=range(1, 50), verbose=False):
    '''
    ruptures 패키지를 사용한 changepoint detection.
    Penalty value를 변경해가며 changepoint를 찾고 빈도가 가장 높은 changepoint를 반환.
    
    Args:
      X          array (n x x) - pcm을 통째로 넣으면 터짐, rms 등으로 줄여서 넣어야 함
      use_diff   np.diff 후 changepoint 추정 (default)
    
    Returns:
      bkpts <list>, states <np.array>, steady <int>
    '''
    
    # model & search range
    model = rpt.Pelt(model=pelt_model, jump=10)
    
    # use_diff - 차분을 사용
    X_ = np.pad(np.diff(X), ((0,0),(0,1)), 'edge') if use_diff else X

    # pen에 따른 Breakpoint 계산 - 빈도 높은 no. of bkpts 선택
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
                bkpts, n_max = b, n
        else:
            n, l = 1, l_b

    # State Array 생성 - [0, 0, 1, 1, 1, ..., 2, 2]
    bkpt_prev = 0
    states = []
    for lab, bkpt in enumerate(bkpts):
        states += [lab] * (bkpt - bkpt_prev)
        bkpt_prev = bkpt
    states = np.array(states, dtype=np.int)
    
    # Steady 선정 - 변동이 가장 작은 한 개 구간이 steady
    std_min = np.Inf
    for s in sorted(set(states)):
        std = X[:, states==s].std()
        if std < std_min:
            steady, std_min = s, std
    
    # Verbose
    if verbose:
        print(f"Check Changepoints:")
        print(f"  - {len(bkpts)} sections estimated, 0-{'-'.join([f'(section {str(i)})-{str(x)}' for i, x in enumerate(bkpts)])}")
        
    return bkpts, states, steady
