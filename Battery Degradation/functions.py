def interpolate_battery(awc, soc, delta):
    import numpy as np
    soc_delta = np.arange(0, 1, 1/delta)
    awc_interpolated = np.interp(soc_delta, soc[::-1], awc)

    return awc_interpolated, soc_delta[::-1]
