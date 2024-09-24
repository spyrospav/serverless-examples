
import time
IMPORT_START_TIME = time.time()
import numpy as np
import pandas as pd
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
def handler(event, context):
    lib_version = {'numpy': np.__version__, 'pandas': pd.__version__}

    sales = [{'account': 'Jones LLC', 'Jan': 150, 'Feb': 200, 'Mar': 140},
             {'account': 'Alpha Co', 'Jan': 200, 'Feb': 210, 'Mar': 215},
             {'account': 'Blue Inc', 'Jan': 50, 'Feb': 90, 'Mar': 95}]
    df = pd.DataFrame(sales)
    print(df)
    return {"import_time": IMPORT_END_TIME - IMPORT_START_TIME}
