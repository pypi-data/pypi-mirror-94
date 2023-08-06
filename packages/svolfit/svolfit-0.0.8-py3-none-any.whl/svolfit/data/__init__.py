import pandas as pd
import os

def get_test_data():
    
    dir_name = os.path.dirname(__file__)
    file_path = os.path.join(dir_name, 'test_path.csv')

    series=pd.read_csv(file_path,index_col=0)

    return series