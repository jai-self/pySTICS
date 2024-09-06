import numpy as np


def soil_temperature(tcultmin, tcultmax, tcult_prev, temp_min, depth, diftherm, tsol_i_prev):
    '''
    This module computes soil temperature for every soil layers (cm by cm).
    See Section 10.2 of STICS book.
    '''
    
    # Daily thermal amplitude
    amplsurf = tcultmax - tcultmin
    thermamp = (7.272e-5/2 / diftherm)**(1/2)

    # Daily thermal amplitude and soil temperature for each soil layer
    amplz_i = np.empty(depth)
    amplz_i[:] = np.nan
    tsol_i = np.empty(depth)
    tsol_i[:] = np.nan

    for z in range(depth):
        tsol_i[z] = tsol_i_prev[z] - np.exp(-(z+1) * thermamp) * (tcult_prev - temp_min) + 0.1 * (tcult_prev - tsol_i_prev[z])
        amplz_i[z] = amplsurf * np.exp(-(z+1) * thermamp)
        tsol_i[z] = tsol_i[z] + amplz_i[z] / 2

    return amplsurf, amplz_i, tsol_i