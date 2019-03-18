# -*- coding: utf-8 -*-
from datetime import datetime
from TKHelper import *
import pandas as pd
import glob

if __name__ == "__main__" :
    try:
        path = input("Input Folder Path : ")
        log_files = glob.glob(path + "/*.txt")
        if log_files:
            tk = TKHelper()
            str_dt_format = '%Y-%m-%d %H:%M:%S.%f'
            try:
                for file in log_files:
                    print("*************************************************")
                    print("File Name :", file)
                    print("*************************************************")
                    with open(file) as fn:
                        line = fn.readline()
                        line_count = 1
                        result_gate_open_close = []
                        result_state_change_inductor1 = []
                        result_state_change_inductor2 = []
                        data_dt_gate_open = ""
                        data_dt_induc1_state_true = ""
                        data_dt_induc2_state_true = ""
                        while line:
                            data = line.strip().split(' : ')
                            dt = data[0]
                            output = data[1]
                            
                            # For Gate Open-Close
                            if output == "gate opened":
                                data_dt_gate_open = datetime.strptime(dt, str_dt_format)
                            if output == "gate closed":
                                if data_dt_gate_open != "":
                                    data_dt_gate_close = datetime.strptime(dt, str_dt_format)
                                    data_dt_diff = data_dt_gate_close - data_dt_gate_open
                                    result_gate_open_close.append(data_dt_diff)
                                
                            # For State Change on First Inductor
                            if output == "Inductor 1 state: True.":
                                data_dt_induc1_state_true = datetime.strptime(dt, str_dt_format)
                            if output == "Inductor 1 state: False.":
                                if data_dt_induc1_state_true != "":
                                    data_dt_induc1_state_false = datetime.strptime(dt, str_dt_format)
                                    data_induc1_dt_diff = data_dt_induc1_state_false - data_dt_induc1_state_true
                                    result_state_change_inductor1.append(data_induc1_dt_diff)
                                
                            # For State Change on Second Inductor
                            if output == "Inductor 2 state: True.":
                                data_dt_induc2_state_true = datetime.strptime(dt, str_dt_format)
                            if output == "Inductor 2 state: False.":
                                if data_dt_induc1_state_true != "":
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
                        print("==========")
                        print("Max Values")
                        print("==========\n")
                        print(df.max())
                        print()
                        print("==========")
                        print("Min Values")
                        print("==========\n")
                        print(df.min())
                        print()
                        print("===========")
                        print("Mean Values")
                        print("===========\n")
                        print(df.mean())
                        print()
                        print("=============")
                        print("Median Values")
                        print("=============\n")
                        print(df.median())
                        print()
            except IOError:
                print("Error: Cannot Open File.")
        else:
            print("No log text file(s) found.")
    except OSError as err:
        print(err)