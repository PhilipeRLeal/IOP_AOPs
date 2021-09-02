import numpy as np
import pandas as pd

from IOP_AOPs.QAA_analysis import apply_QAA



def test_apply_QAA():
    try:
	    N_samples = 10

	    Bandas = [412, 443, 489, 510, 555, 670]

	    Random_data = np.random.randint(low=0, high=800, size=(N_samples,len(Bandas)))/1000 

	    Rrs_Data = pd.DataFrame(Random_data, columns = Bandas)

	    Rrs_Data.head()

	    QAA_Results = apply_QAA(Rrs_Data)

	    for k, v in QAA_Results.items():
	        print(str(k), '\n'*3, '-'*50,'\n', v, '\n'*3)

	    assert isinstance(Rrs_Data, pd.DataFrame)

	except:
		assert False
        
