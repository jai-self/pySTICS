import numpy as np
from pystics.modules.growth.thermal_stress_indices import frost_stress
from pystics.exceptions import pysticsException


def senescence(i, lev, ulai, somtemp, vlaimax, durviei, durvief, senfac_prev, fstressgel,
               nsencour_list, senstress_list, tdevelop_list, durvie_list, durage_list, deltai_bis_list,
                somsenreste_prev, lai0, ndebsen, dltafv_list, ratiosen, forage, msres_prev, msresiduel, msresjaune_prev, codlainet, pfeuilverte_list, dltams_list, dltaisen):
    '''
    This module computes leaf and biomass senescence.
    See section 4.1.2 of STICS book.

    Simplifications compared to STICS :
        - Nitrogen effect on senescence not implemented
    '''

    # Initialize values
    dltamsen, somsenreste, deltamsresen, msresjaune = 0, 0, 0, 0
    msres = msres_prev

    if lev[i] > 0:        
        ind_EMERG = np.where(lev > 0)[0][0]

        # Initialize oldest non-senescent leaf area
        if i == ind_EMERG:
            nsencour_list[i] = i

        # Stress index affecting senescence
        senstress_list[i] = min(senfac_prev, fstressgel)

        if codlainet == 1:
            senstress_list[i] = 1

        # Update lifespan of all non-senescent leaf areas
        for j in range(int(nsencour_list[i]),i):
            durvie_list[j] = min(durvie_list[j], durage_list[j] * min(senstress_list[i], fstressgel))

            # if (amf_list[j] == 1) & (java_inn > 1):
            #     durviesup = durvief * min(durviesupmax, java_inn-1)
            #     durvie_list[j] = durvie_list[j] + durviesup
        
        # Lifespan of leaf area produced on day i
        if (ulai <= vlaimax):
            durage_list[i] = (durviei)
        else:
            durage_list[i] = durviei + (durvief - durviei) * (ulai - vlaimax) / (3 - vlaimax)

        durvie_list[i] = durage_list[i] * min(senstress_list[i], fstressgel)

        # if (amf_list[i] == 1) & (java_inn > 1):
        #     durviesup = durvief * min(durviesupmax, java_inn-1)
        #     durvie_list[i] = durvie_list[i] + durviesup

        # Senescence of residual biomass for forage crops
        if forage:
            if msres_prev > 0:
                deltamsresen = msresiduel * ratiosen * tdevelop_list[i] / durviei
                msres_tmp = max(0, msres_prev - deltamsresen)
                deltamsresen = msres_prev - msres_tmp
                msres = msres_prev - deltamsresen
            
            # Cumulated senescent residual biomass
            msresjaune = msresjaune_prev + deltamsresen
            
        
        deltai_disappears = True
        nb_deltai_senescent = 0
        

        if somtemp > durvie_list[i]:

            if ndebsen == 0: # first day of senescence
                ndebsen = i
                if codlainet == 2:
                    dltaisen = dltaisen + lai0
                dltamsen =  pfeuilverte_list[i] * ratiosen * dltams_list[i]

            somsen = somsenreste_prev + tdevelop_list[int(nsencour_list[i])+1:i+1].sum()
            while deltai_disappears: # as long as deltai become senescent, we check senescence of following day (several deltai can become senescent on day i)
                
                # Oldest non-senescent deltai
                j = int(nsencour_list[i]) + nb_deltai_senescent

                # Compare development temperature to leaf area lifespan, and trigger senescence
                if (somsen >= durvie_list[j]) & (j < i):
                    nb_deltai_senescent +=1
                    if codlainet == 2:
                        dltaisen = dltaisen + deltai_bis_list[j]
                    somsen = somsen - durvie_list[j]
                    if somsen < 0:
                        somsen = 0
                        nb_deltai_senescent = nb_deltai_senescent - 1
                        break

                    dltamsen = dltamsen + ratiosen * pfeuilverte_list[j] * dltams_list[j]
                else:
                    deltai_disappears = False
            
            somsenreste = somsen
        
        # Update oldest non-senescent deltai
        nsencour_list[i] = nsencour_list[i] + nb_deltai_senescent

    return nsencour_list, durage_list, senstress_list, tdevelop_list, durvie_list, dltaisen, somsenreste, ndebsen, somtemp, dltamsen, deltamsresen, msres, msresjaune, durvie_list[i]

def senescence_stress(lev_i, ulai, vlaimax, tcultmin_prev, tgeljuv10, tgeljuv90, tgelveg10, tgelveg90, tletale, tdebgel, codgeljuv, codgelveg):
    '''
    This module computes frost stress affecting senescence.
    '''
    
    fstressgel = 1

    if lev_i > 0:
        
        # Frost stress
        if (
            ulai < vlaimax
        ):  # si on est avant stade iamf --> fgeljuv
            if codgeljuv == 2:
                fstressgel = frost_stress(tcultmin_prev, tgeljuv90, tgeljuv10, tletale, tdebgel)

        else:  # après stade iamf -> fgelveg
            if codgelveg == 2:
                fstressgel = frost_stress(tcultmin_prev, tgelveg90, tgelveg10, tletale, tdebgel)
    else:
        fstressgel = 1

    return fstressgel

