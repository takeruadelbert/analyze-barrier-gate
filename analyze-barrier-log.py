# -*- coding: utf-8 -*-
from datetime import datetime
from TKHelper import *
import pandas as pd

if __name__ == "__main__" :
    filename = "src/2019-03-01.txt"
    tk = TKHelper()
    str_dt_format = '%Y-%m-%d %H:%M:%S.%f'
    try:     
        with open(filename) as fn:
            line = fn.readline()
            line_count = 1
            result_gate_open_close = []
            result_state_change_inductor1 = []
            result_state_change_inductor2 = []
            while line:
                data = line.strip().split(' : ')
                dt = data[0]
                output = data[1]
                
                # For Gate Open-Close
                if output == "gate opened":
                    data_dt_gate_open = datetime.strptime(dt, str_dt_format)
                if output == "gate closed":
                    data_dt_gate_close = datetime.strptime(dt, str_dt_format)
                    data_dt_diff = data_dt_gate_close - data_dt_gate_open
                    result_gate_open_close.append(data_dt_diff)
                    
                # For State Change on First Inductor
                if output == "Inductor 1 state: True.":
                    data_dt_induc1_state_true = datetime.strptime(dt, str_dt_format)
                if output == "Inductor 1 state: False.":
                    data_dt_induc1_state_false = datetime.strptime(dt, str_dt_format)
                    data_induc1_dt_diff = data_dt_induc1_state_false - data_dt_induc1_state_true
                    result_state_change_inductor1.append(data_induc1_dt_diff)
                    
                # For State Change on Second Inductor
                if output == "Inductor 2 state: True.":
                    data_dt_induc2_state_true = datetime.strptime(dt, str_dt_format)
                if output == "Inductor 2 state: False.":
                    data_dt_induc2_state_false = datetime.strptime(dt, str_dt_format)
                    data_induc2_dt_diff = data_dt_induc2_state_false - data_dt_induc2_state_true
                    result_state_change_inductor2.append(data_induc2_dt_diff)
                
                line = fn.readline()
                line_count += 1
                
            # Convert to Pandas Data
            panda_data = {
                    'Open Close Gate': pd.Series(result_gate_open_close),
                    'State Change of First Inductor': pd.Series(result_state_change_inductor1),
                    'State Change of Second Inductor': pd.Series(result_state_change_inductor2)
            }
            
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