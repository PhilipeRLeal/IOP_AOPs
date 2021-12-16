
from math import *

def aCDOM_300 (S_275_to_295):
	
	""" Funcao que retorna aCDOM(300) (1/m) com base nos valores de S(275-295)
		
		Referência do cálculo :

			CAO, F. et al. Remote sensing retrievals of colored 
			dissolved organic matter and dissolved organic carbon
			dynamics in North American estuaries and their margins. 
			Remote Sensing of Environment, v. 205, n. April 2017,
			p. 151–165, 2018.

	"""

	aCDOM_300 = (exp( -15.05 - 33.95 * S_275_to_295)
				+ exp(-1.502 - 104.3 * S_275_to_295)

	return aCDOM_300
