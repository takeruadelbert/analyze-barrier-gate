# -*- coding: utf-8 -*-
from datetime import datetime
from TKHelper import *
import pandas as pd

if __name__ == "__main__" :
    filename = "src/2019-03-01.txt"
    tk = TKHelper()
    try:     
        with open(filename) as fn:
            line = fn.readline()
            line_count = 1
            result_gate_open_close = []
            while line:
                data = line.strip().split(' : ')
                dt = data[0]
                output = data[1]
                
                if output == "gate opened":
                    data_dt_gate_open = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f')
                if output == "gate closed":
                    data_dt_gate_close = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f')
                    data_dt_diff = data_dt_gate_close - data_dt_gate_open
                    result_gate_open_close.append(data_dt_diff)
                line = fn.readline()
                line_count += 1
                
            # Convert to Pandas Data
            panda_data = {'Open Close Gate': pd.Series(result_gate_open_close)}
            
            # Create DataFrame
            df = pd.DataFrame(panda_data)
            
            # ======
            # OUTPUT
            # ======
#            tk.PrintDataResult(result_gate_open_close)
            print("==========")
            print("Max Values")
            print("==========\n")
            print(df.max())
            print("\n*********************************")
            print("==========")
            print("Min Values")
            print("==========\n")
            print(df.min())
            print("\n*********************************")
            print("===========")
            print("Mean Values")
            print("===========\n")
            print(df.mean())
            print("*********************************")
            print("=============")
            print("Median Values")
            print("=============\n")
            print(df.median())
            print("\n*********************************")
    except IOError:
        print("Error: Cannot Open File.")