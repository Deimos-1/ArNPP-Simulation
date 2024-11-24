from variables import Variables

## GRAPH UPDATE
def axes_update(flux_values: dict, v: Variables):
    """
    Returns the new axes values (shifts the dictionary and add current value)
    :flux_values: a dictionnary of the flux values, entry 0 is the current flux.
    """
    ## we shift all values
    for key in flux_values.keys():
        if key < 0:
            flux_values[key] = flux_values[key+1]
        if key == 0:
            flux_values[key] = v.neutron_flux
    return flux_values


    
