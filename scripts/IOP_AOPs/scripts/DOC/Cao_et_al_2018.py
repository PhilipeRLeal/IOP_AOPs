from math import *

def get_DOC(aCDOM_300, S_275_to_295):
	
	""" Função que retorna DOC (μmol L−1) com base nos valores de aCDOM(300) e S(275-295).

		A variabilidade (R2) desta função varia entre 0.92 e 0.94.
		A função foi otimizada para um range de DOC variando entre [73–953 μmol L−1]
	
		Referência do cálculo :

			CAO, F. et al. Remote sensing retrievals of colored 
			dissolved organic matter and dissolved organic carbon
			dynamics in North American estuaries and their margins. 
			Remote Sensing of Environment, v. 205, n. April 2017,
			p. 151–165, 2018.

	"""

	DOC = aCDOM_300 / (exp(-15.05 - (33,95 * S_275_to_295)) 
		  + exp(-1,502 - (104,3 * S_275_to_295)))
	print("\n\nDOC: ", DOC, " μmol L−1")

	return DOC