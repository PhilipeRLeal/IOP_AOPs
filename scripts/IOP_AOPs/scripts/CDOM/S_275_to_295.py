
def S_275_to_295(Rrs_443, Rrs_448, Rrs_531, Rrs_555, Rrs_667):
	from math import *
	"""
		Função que retorna S(275-295) com base nos valores de reflectância 
		dos sensores MERIS e MODIS-A NASA Ocean Biology Distributed Active 
		Archive Center (OB-DAAC; https://oceancolor.gsfc.nasa.gov)
		
		A função é baseada no modelo de Cao et al (2018), em que os autores se utilizaram 
		da regressão multivariada stepwise a partir do sensor Meris e MODIS-Aqua 
		para obtenção dos coeficientes da regressão e estimativa de S(275-295)
		


		Referência do cálculo :

			CAO, F. et al. Remote sensing retrievals of colored 
			dissolved organic matter and dissolved organic carbon
			dynamics in North American estuaries and their margins. 
			Remote Sensing of Environment, v. 205, n. April 2017,
			p. 151–165, 2018.

	"""

	a = -0.0537
	b = 0.2689
	c = 0.1017
	d = -0.2097
	e = -0.0893
	f = -3.6853

	ln_S_275_to_295 = a * ln(Rrs_443) + b * ln(Rrs_448) 
					  + c* ln(Rrs_531) + d * ln(Rrs_555)
					  + e * ln(Rrs_667) + f

	S_275_to_295 = exp(ln_S_275_to_295)

	return S_275_to_295
