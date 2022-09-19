import sys
import os
import numpy as np
from scipy.optimize import minimize
import ckk5_prelab as pb

optimizations = 0

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
			print(f"{key}: {sweep_params[key][param_iter]}")
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
	os.system(f"hspice {target_spice} > {target_spice}.dump")
	data = pb.import_data(output_file)
	#optimizations += 1
	print(f"output: {data[target_name][0]}")
	return float(data[target_name][0])

def write_amplifiers(output, nodes):
	file_handle = open(output, 'w')
	for i in range(nodes - 1):
		line = f"XIn_{i} In_{i} In_{i+1} vdd vss inv size =\'size_{i}\'\n"
		file_handle.write(line)
	file_handle.write(f"XIn_{nodes-1} In_{nodes -1} output vdd vss inv size =\'size_{nodes-1}\'\n")

if __name__ == "__main__":
	
	initial_value = [1.8, 5.5, 13.6]
	stage_names = ["size_" + str(i) for i in range(len(initial_value))]
	bounds = [(1,64) for i in initial_value]

	write_amplifiers("amplifier.sp", len(initial_value))
	
	arguments = ("ckk5_critical_path.sp",
					"sweep_params.sp",
					"sweep_params",
					stage_names,
					"delay",
					"ckk5_critical_path.mt0")
	
	print(minimize(Optimize_Function, initial_value,
		method='Nelder-Mead', 
		args = arguments, 
		bounds = bounds,
		options={'disp':True}))
