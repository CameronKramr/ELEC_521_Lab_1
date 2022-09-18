import sys
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
	
	for i in range(len(sweep_params[0])):
		for key in keys
			file_obj.write(f" {sweep_params[key][i]}")
		file_obj.write('\n')
	file_obj.write(".ENDDATA")
	file_obj.close()
if __name__ == "__main__":
	print("Hello world")
	test_params = {"len1", "len2", "len3"}
	test_params["len1"] = [i for i in range(10)]
	test_params["len2"] = [i*i for i in range(10)]
	test_params["len3"] = [i*2 for i in range(10)]
	
	write_sweep_params("test.sp", "example", test_params)
