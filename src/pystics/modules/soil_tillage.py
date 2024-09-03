



def soil_tillage_impact_on_soil_water(hur_i, proftrav):
    '''
    This module computes soil tillage impact on soil water content.
    '''

    tot_hur = hur_i[0:proftrav].mean()
    tmix = 1
    for z_index in range(proftrav):
        hur_i[z_index] = (1.-tmix) * hur_i[z_index] + tmix* tot_hur
    
    return hur_i