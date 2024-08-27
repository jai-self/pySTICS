



def cumultative_partitioning(lev, mafeuil, matigestruc, codeperenne, masec, restemp0, resplmax, densite, remobres, deltai, slamin, ratiotf, codeindetermin, dltams, cumdltares_prev):
    '''
    This module computes the reserves remobilisation with the cumulative partitioning approach (see chapter 7 of STICS book with code_acti_reserves = 2).
    '''

    #########################
    ### Vegetative organs ###
    #########################

    # Reserve = total biomass - leaves / stem / harvested organs = biomass that can be accumulated or mobilized
    if (lev == 0) and (codeperenne == 2): 
        restemp = restemp0
    elif lev == 1:
        restemp = max(0, masec - mafeuil - matigestruc) #- mafruit_prev - maenfruit_prev
    else:
        restemp = 0
        
    # Reserve limit --> sink/source applied if this limit is reached
    restempmax = 10 * resplmax * densite
    if restemp > restempmax:
        dltams = 0
    
    dltarestemp = max(0, restemp-restempmax)

    ##############################
    ### Reserves remoblisation ###
    ##############################

    # 1. Source / sink ratio

    # Sink strength of vegegative organs
    fpv = (
        deltai
        * 10000
        / (slamin / (1 + ratiotf))
    )

    # Sink strength of reproductive organs (only for indeterminate growth plants)
    if codeindetermin == 1:
        fpft = 0
    else:
        fpft = 0 # TODO

    # Source / sink ratio (first computation)
    sourcepuits1 = min(1,
        dltams * 100
        / (fpv + fpft)
        if fpv + fpft != 0
        else 1
    )

    # 2. Reserves mobilisation if source/sink ratio < 1

    # Remobilised reserved
    if sourcepuits1 < 1:
        remob = (fpv + fpft) / 100 - dltams
        remob = min(remob, remobres * restemp)
        remobilj = min(remob, restemp)
        if cumdltares_prev < restemp0:
            dltaremobil = min(remob,restemp)
            restemp = restemp - dltaremobil
            remobilj = 0
        else:
            remobilj = min(remob, restemp)
            dltaremobil = 0

    else:
        dltaremobil = 0
        remobilj = 0
    
    # Sink / source ratio after remobilisation
    sourcepuits = (dltams + dltaremobil) / (fpv + fpft) if fpv + fpft != 0 else 1 # same as sourcepuits1 here ?

    cumdltares = cumdltares_prev + remobilj + dltaremobil

    return dltaremobil, restemp, dltams, fpv, sourcepuits, dltarestemp, remobilj, cumdltares