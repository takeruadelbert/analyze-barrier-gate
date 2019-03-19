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
            log_files.sort()
            tk = TKHelper()
            str_dt_format = '%Y-%m-%d %H:%M:%S.%f'
            try:
                for file in log_files:
                    print("\n*************************************************")
                    print("File Name :", file)
                    print("*************************************************")
                    with open(file) as fn:
                        line = fn.readline()
                        line_count = 1
                        result_gate_open_close = []
                        result_state_change_inductor1 = []
                        result_state_change_inductor2 = []
                        temp_reverse_state_change_inductor1 = []
                        result_reverse_state_change_inductor1 = []
                        temp_reverse_state_change_inductor2 = []
                        result_reverse_state_change_inductor2 = []
                        data_dt_gate_open = ""
                        data_dt_induc1_state_true = ""
                        data_dt_induc2_state_true = ""
                        data_dt_induc1_state_false = ""
                        data_dt_induc2_state_false = ""
                        gate_opened_valid = False
                        gate_closed_valid = False
                        while line:
                            data = line.strip().split(' : ')
                            dt = data[0]
                            output = data[1]
                            
                            # For Gate Open-Close
                            if output == "gate opened":
                                gate_opened_valid = True
                                data_dt_gate_open = datetime.strptime(dt, str_dt_format)
                            if output == "gate closed":
                                gate_closed_valid = True
                                if data_dt_gate_open != "":
                                    data_dt_gate_close = datetime.strptime(dt, str_dt_format)
                                    data_dt_diff = data_dt_gate_close - data_dt_gate_open
                                    result_gate_open_close.append(data_dt_diff)
                                
                            # For State Change on First Inductor
                            if output == "Inductor 1 state: True.":
                                data_dt_induc1_state_true = datetime.strptime(dt, str_dt_format)
                                if data_dt_induc1_state_false != "":
                                    reverse_data_induc1_dt_diff = data_dt_induc1_state_true - data_dt_induc1_state_false
                                    if str(reverse_data_induc1_dt_diff) == "-1 day, 23:44:48.665724":
                                        print(data_dt_induc1_state_true)
                                        print(data_dt_induc1_state_false)
                                    temp_reverse_state_change_inductor1.append(reverse_data_induc1_dt_diff)
                            if output == "Inductor 1 state: False.":
                                if data_dt_induc1_state_true != "":
                                    data_dt_induc1_state_false = datetime.strptime(dt, str_dt_format)
                                    data_induc1_dt_diff = data_dt_induc1_state_false - data_dt_induc1_state_true
                                    result_state_change_inductor1.append(data_induc1_dt_diff)
                                
                            # For State Change on Second Inductor
                            if output == "Inductor 2 state: True.":
                                data_dt_induc2_state_true = datetime.strptime(dt, str_dt_format)
                                if data_dt_induc2_state_false != "":
                                    reverse_data_induc2_dt_diff = data_dt_induc2_state_true - data_dt_induc2_state_false
                                    temp_reverse_state_change_inductor2.append(reverse_data_induc2_dt_diff)
                            if output == "Inductor 2 state: False.":
                                if data_dt_induc2_state_true != "":
                                    data_dt_induc2_state_false = datetime.strptime(dt, str_dt_format)
                                    data_induc2_dt_diff = data_dt_induc2_state_false - data_dt_induc2_state_true
                                    result_state_change_inductor2.append(data_induc2_dt_diff)
                                    
                            # For Reverse State Change on First and Second Inductor (False -> True)
                            if gate_opened_valid and gate_closed_valid:
                                result_reverse_state_change_inductor1.extend(temp_reverse_state_change_inductor1)
                                result_reverse_state_change_inductor2.extend(temp_reverse_state_change_inductor2)
                                gate_opened_valid = False
                                gate_closed_valid = False
                                temp_reverse_state_change_inductor1 = []
                                temp_reverse_state_change_inductor2 = []
                            
                            line = fn.readline()
                            line_count += 1
                            
                        # Convert to Pandas Data
                        panda_data = {
                                'Open Close Gate': pd.Series(result_gate_open_close),
                                'State Change (True -> False) of First Inductor': pd.Series(result_state_change_inductor1),
                                'State Change (True -> False) of Second Inductor': pd.Series(result_state_change_inductor2),
                                'State Change (False -> True) of First Inductor': pd.Series(result_reverse_state_change_inductor1),
                                'State Change (False -> True) of Second Inductor': pd.Series(result_reverse_state_change_inductor2)
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