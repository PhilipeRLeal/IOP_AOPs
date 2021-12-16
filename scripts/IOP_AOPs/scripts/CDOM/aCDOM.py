from math import *

def aCDOM_Cao_et_al_2018(λ, Rrs, Referencia=False):
	
	""" Variáveis:
		λ: lambda em que o aCDOM será calculado
		Rrs: Dicionário de Reflectância de sensoriamento remoto de entrada.
			Rrs deverá conter valores para Rrs(443, 488, 531, 555 e 667)
		Referencia: retorna um print da referencia do artigo com a equação.
			Por padrão é falso. Se !=, retorna print()
		Retorna: aCDOM(λ especificado)

		Referência do cálculo :

			CAO, F. et al. Remote sensing retrievals of colored 
			dissolved organic matter and dissolved organic carbon
			dynamics in North American estuaries and their margins. 
			Remote Sensing of Environment, v. 205, n. April 2017,
			p. 151–165, 2018.

		Erro estimado segundo Cao et al (2018): < 28%
	"""
	if Referencia !=False:
		print('\n\n', 'CAO, F. et al. Remote sensing retrievals of colored \
			dissolved organic matter and dissolved organic carbon \
			dynamics in North American estuaries and their margins.  \
			Remote Sensing of Environment, v. 205, n. April 2017, \
			p. 151–165, 2018.', '\n\n')

	if λ== 300: # 300 nm

		α=−0.0206
		β=−0.6128
		γ=−0.0070
		δ=−0.4944
		ε=0.9362
		ζ=0.9666

	if λ==355: # 355nm

		α=0.0376
		β=−0.8714
		γ=−0.0352
		δ=−0.2739
		ε=0.9591
		ζ=−0.1071


	ln(aCDOM(λ)) = α*ln(Rrs[443]) + β * ln(Rrs[488])
					+ γ * ln(Rrs[531]) + δ * ln(Rrs[55])
					+ ε * ln(Rrs[667]) + ζ

	return exp(aCDOM(λ))