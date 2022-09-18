import sys
import os
import numpy as np
from scipy.optimize import minimize
import ckk5_prelab as pb

def write_sweep_params(filename, param_name, sweep_params):
	keys = list(sweep_params.keys())
	
	file_obj = open(filename, 'w')
	file_obj.write(f".DATA {param_name}")
	
	for key in keys:
		file_obj.write(f" {key}")
	file_obj.write('\n')
	
	#print(keys)
	for param_iter in range(len(sweep_params[keys[0]])):
		for key in keys:
			file_obj.write(f" {sweep_params[key][param_iter]}")
		file_obj.write('\n')
	file_obj.write(".ENDDATA")
	file_obj.close()

def Optimize_Function(x, *args):
	target_spice = args[0]
	param_file = args[1]
	param_name = args[2]
	vector_names = args[3]
	target_name = args[4]
	output_file = args[5]
	
	#convert the parameters into a dictionary form
	params = {}
	for iter, item in enumerate(x):
		params[vector_names[iter]] = [item]
	
	write_sweep_params(param_file, param_name, params)
	os.system(f"echo {target_spice}")
	data = pb.import_data(output_file)
	return float(data[target_name][0])

if __name__ == "__main__":
	arguments = ("ckk5_critical_path.sp",
					"sweep_params.sp",
					"sweep_params",
					["size_stage_1", "size_stage_2", "size_stage_3"],
					"delay",
					"ckk5_critical_path.mt0")
	bounds = [(1,20),(1,20),(1,20)]
	initial_value = [1, 1, 1]
	
	minimize(Optimize_Function, initial_value, args = arguments, bounds = bounds)
