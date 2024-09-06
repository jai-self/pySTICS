import numpy as np

def harvested_organs_number(i, dltams_list, nbjgrain, cgrainv0, cgrain, nbgrmax, nbgrmin):
    '''
    This module computes the number of harvested organs.
    See section 8.1.1 of STICS book.
    '''
    
    # Average biomass production on the grains/fruits formation period (before filling start)
    vitmoy = (dltams_list[i - nbjgrain + 1 : i+1].sum() / nbjgrain)*100

    # Grains/fruits number
    nbgrains = (cgrainv0 + cgrain * vitmoy) * nbgrmax
    nbgrains = min(nbgrains, nbgrmax) 
    nbgrains = max(nbgrains, nbgrmin)

    return vitmoy, nbgrains

def frost_reduction_harvested_organs(i, drp_list, nbgrains_prev, fgelflo, pgrain_list, nbgraingel_list):
    '''
    This module computes the mass of harvestable organs destroyed by frost (pgraingel) during grains/fruits filling.
    See section 8.1.1 of STICS book.
    '''

    ind_drp = np.where(drp_list > 0)[0][0]
    nbgraingel_list[i]  = nbgrains_prev * (1 - fgelflo)
    nbgrains =  (nbgrains_prev - nbgraingel_list[i])
    pgraingel = (pgrain_list.loc[ind_drp:i-1] * nbgraingel_list[ind_drp+1:i+1]).sum()

    return nbgrains, nbgraingel_list, pgraingel


def carbon_harvest_index(i, ircarb_list, mat_list, drp_list, codeir, vitircarb, vitircarbt, irmax, somcourdrp):
    """
    This module computes the harvest index (ircarb) during fruit filling.
    See section 8.1.1 of STICS book.
    """
    if drp_list[i-1] > 0:
        ind_drp = np.where(drp_list > 0)[0][0]
        if codeir == 1:
            ircarb_list[i]  = np.minimum(vitircarb * (i - ind_drp +1), irmax)
        else:
            ircarb_list[i]  = vitircarbt * somcourdrp
        if mat_list[i-1] > 0:
            ind_mat = np.where(mat_list > 0)[0][0]
            ircarb_list[i] = ircarb_list[ind_mat]

    return ircarb_list



def harvested_organs_mass(i, ircarb, masec, ircarb_prev, masec_prev, ftempremp, pgrainmaxi, nbgrains, mat_list, deltags_list, mafruit_prev, pgrain_prev, nbgraingel):
    '''
    This module computes the mass of harvested organs (deltags) between fruit filling start (drp) and physiological maturity (mat), reduced by the mass of frozen grains.
    See section 8.1.1 of STICS book.
    '''

    # Daily grain/fruit mass increase
    deltags_list[i] = (ircarb * masec - ircarb_prev * masec_prev) * ftempremp
    if mat_list[i] > 0:
        deltags_list[i] = 0

    # Cumulated grains/fruits mass, reduced with frozen grains
    mafruit = mafruit_prev + deltags_list[i] - pgrain_prev * nbgraingel

    if mafruit > (pgrainmaxi * nbgrains / 100):
        mafruit = pgrainmaxi * nbgrains / 100
        deltags_list[i] = 0

    # Average mass per grain/fruit
    if nbgrains > 0:
        pgrain = np.minimum(mafruit / nbgrains, pgrainmaxi)
    else:
        pgrain = 0

    return mafruit, deltags_list, pgrain


def grains_water_content(i, tcult_list, temp_list, debdes_list, h2ofrvert, deshydbase, tempdeshyd):
    '''
    This module computes grains/fruits water content (teaugrain).
    See section 8.2.1 of STICS book.
    '''

    if debdes_list[i] == 0:
        teaugrain = h2ofrvert
    else:
        ind_debdes = np.where(debdes_list > 0)[0][0]
        teaugrain = h2ofrvert - deshydbase * (i - ind_debdes + 1) - tempdeshyd * (tcult_list[ind_debdes:i] - temp_list[ind_debdes:i]).sum()
    teaugrain = max(0, teaugrain)

    return teaugrain