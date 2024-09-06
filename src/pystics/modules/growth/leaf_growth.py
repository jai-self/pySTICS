import numpy as np


def leaf_growth(i, lev_i, lax_i, drp_i, stlevamf, vlaimax, stamflax, udlaimax, dlaimax, pentlaimax,
                    tcult_prev, tcxstop, tcmax, tcmin, adens, bdens, densite, turfac_prev, phoi, phoi_prev, ratiotf,
                    phobase, rfpi, dlaimin, lai_prev, laicomp, stopfeuille, vmax_prev,
                    codlainet, dltaisenat_prev, fstressgel_prev, laisen_prev, lax, slamin, slamax, dltamsen_prev,
                    dltaisen_prev, lan_i, codephot_part, amf_i, tigefeuil, dltams_prev, codeindetermin, sla_prev, sen, sen_i_prev, somcour, stsenlan, lai_list, dltaremobil_prev, remobilj_prev):
    '''
    This module computes the leaf growth (deltai) and its different components (ulai, tempeff, turfac, densite).
    See section 4.1 of STICS book.
    '''

    deltai, tempeff, ulai, efdensite, deltaimaxi = 0, 0, 0, 1, 0
    vmax = vmax_prev.copy()
    dltaisenat = dltaisenat_prev.copy()

    # Leaf growth stop criteria
    if ((stopfeuille == 'LAX') & (lax_i == 1)): # determinate growth crops
        stopfeuille_stage = 1
    else:
        stopfeuille_stage = 0

    if (lev_i == 1) & (stopfeuille_stage == 0):
        
        # Development effect on leaf growth (ulai)
        if amf_i == 0:
            ulai = 1 + (vlaimax - 1) * somcour / stlevamf

        elif (amf_i > 0) & (lax_i == 0):
            ulai = vlaimax + (3. - vlaimax) * somcour / stamflax

        if ((codeindetermin == 2) & (drp_i > 0)) | (lax_i > 0):
            ulai = udlaimax
        
        # Interplant competition effect on leaf growth
        efdensite = 1
        if ulai > 1:
            if lai_prev < laicomp:
                efdensite = 1
            else:
                if densite == 0:
                    efdensite = 0
                else:
                    efdensite = min(1, np.exp(np.log(densite / bdens) * (adens)))
        else:
            if densite == 0:
                efdensite = 0
            else:
                efdensite = min(1, np.exp(np.log(densite / bdens) * (adens)))
        
        if ulai == 1:
            efdensite = 1

        # Thermal component of leaf growth
        tempeff = max(0, tcult_prev - tcmin)
        if tcxstop >= 100:
            if tcult_prev > tcmax:
                tempeff = tcmax - tcmin
        elif tcult_prev > tcmax:
                tempeff = max(0,(tcmax - tcmin) * (tcult_prev - tcxstop) / (tcmax - tcxstop))
        
        # Development and interplant competition components of leaf growth
        if (udlaimax == 3) | (ulai <= udlaimax):
            deltai = efdensite * densite * dlaimax * (dlaimin + (1 - dlaimin) / (1 + np.exp(pentlaimax * (vlaimax - ulai))))
            vmax = deltai
        else:    
            deltai = vmax * (1 - (ulai - udlaimax) / (3 - udlaimax))**2
        
        deltai = deltai * tempeff * turfac_prev

        ratiotf = tigefeuil
        if codeindetermin == 2: # splai not implemented
            
            # Negative effect of photoperiod during days shortening period
            if codephot_part == 1:
                if phoi < phobase:
                    rfpi = 0
                    deltai = deltai * rfpi
                    ratiotf = tigefeuil * rfpi
                else:
                    deltai = deltai * rfpi
        else:
        
            # Max deltai
            sbvmax = slamax / (1.0 + tigefeuil)
            deltaimaxi = (dltams_prev + remobilj_prev) * sbvmax / 100. # not dltaremobil like in 4.7
        
            if (amf_i > 0):
                deltai = min(deltai, deltaimaxi)

    elif lev_i == 1:
        ulai = 3
    
    if (codlainet == 1) & (codeindetermin == 1) & (lax_i > 0):
        deltai = 0
    
    # Senescence between sen and lan for codlainet = 1
    if codlainet == 1:
        lai = lai_prev + deltai - dltaisenat_prev

        if (sen_i_prev == 0) & (sen[i] == 1):
            lai = lai_prev
            lai_list[i] = lai_prev

        if (sen[i] == 1) & (lan_i == 0):
            lai = lai_list[np.where(sen > 0)[0][0]] * (1-somcour/stsenlan) # TODO
            dltaisenat = lai_prev - lai
            if (lai <= 0) & (lan_i == 0):
                lan_i = 1
                lai = 0
        if lan_i == 1:
            lai = 0
    else:
        lai = max(lai_prev + deltai - dltaisen_prev, 0)

    mafeuilverte = lai / slamax * 100
    
    # Leaf senescence because of stress for codlainet == 1
    if (codlainet == 1) & (lai > 0):
        if (tcult_prev < tcmin) | (fstressgel_prev < 1):
            dltaisen = dltamsen_prev /100 * sla_prev # tustress not computed
            lai = max(lai - dltaisen, 0)
            dltaisen = dltaisen + dltaisenat

        else:
            dltaisen = dltaisenat
    else:
        dltaisen = 0

    # Cumulated leaf senescence
    if codlainet == 1:
        laisen = laisen_prev + dltaisen # dltaisen i-1 if codlainet = 2, i if codlainet = 1
    else:
        laisen = laisen_prev + dltaisen_prev


    if (lai <= 0) & (lan_i == 0) & (lax == 1):
        sen[i] = 1
        lan_i = 1

    return deltai, tempeff, ulai, efdensite, vmax, lai, mafeuilverte, dltaisen, dltaisenat, laisen, lan_i, sen[i], ratiotf, stopfeuille_stage, deltaimaxi