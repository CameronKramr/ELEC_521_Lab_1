import sys


#function to find the headers and put the lines into a list
def collect_header(file_target, MAX_SEARCH = 100, last_header = 'alter#'):
	#get first line
	line = file_target.readline()
	#Find the first header
	count = 0
	while(line):	#The readline function returns None if there are no more lines
		#check if there are no more comments. Easy to break, but it works on all provided files
		if line[0] == ' ' and len(line) >= 2 and line[1] != ' ':
			break
		line = file_target.readline()
		if(count > MAX_SEARCH):
			return None
	#this line contains a header so it is stored
	output = [line]
	
	#Find all remaining headers
	count = 0
	while(line):
		#If the last header is in this line, it is time to stop
		if(last_header in line):
			break
		line = file_target.readline()
		#Append line to the output list
		output.append(line)
			
		#check to stop infinite loops
		if(count > MAX_SEARCH):
			return None
	#Output a list of lines
	return output

#Takes a list of header strings and converts them to a list of headers and a count of the columns
def determine_rows(header_rows):
	#initialize
	col_parts = []	#List of column headers
	
	#Loop through each input row
	for header_row in header_rows:
		#Split each string on white space. Good enough for the provided examples
		row = header_row.split()
		col_parts += row
		
	#Return the required information
	return col_parts, len(header_rows)

def parse_data(File_Target, Col_Parts, Header_Rows):
	#Grab a line from the File_Target. It's assumed that the next line is the start of the data (since we're the only ones that have used it)
	line = File_Target.readline()
	output = {}
	
	#Build output dictionary of lists
	for item in Col_Parts:
		output[item] = []
	
	#Loop until line == None (meaning the end of file)
	while(line):
		line_parts = []
		
		#Grab one row of data for each row of header
		for item in range(Header_Rows):
			#Line parts is a list formed by spliting the line at white space
			line_parts += line.split()
			line = File_Target.readline()
			
		#Iterate over every item in the line_parts list
		for line_iter, line_item in enumerate(line_parts):
			#Items are entered sequentially with some line wraps so there are
			#only 4 columns of data. These line wraps are the same as the
			#headers so they match 1-1 when looped in this way 
			
			#index the output dictionary at the current key and
			#append the current line_item to that list
			if('failed' in line_item):
				line_item = 'Nan'
			output[Col_Parts[line_iter]].append(line_item)
	return output

def print_data(data_file, Keys = None, seperator = ','):
	#If no keys were provided, use them all
	#It's (far) easier to just collect all the data and only
	#print out what's desired
	if(Keys == None):
		Keys = list(data_file.keys())	#Get all the keys

	#Print the headers
	line = ""
	for key in Keys:
		#Building a string with all the keys in it seperated by the seperator
		line += str(key) + seperator
	#Print the string removing the last seperator (an un-matched seperator)
	print(line[:-len(seperator)])
	
	#Loop through all the data. Each column is assumed to have the same amount
	#of data
	for i in range(len(data_file[Keys[0]])):
		#Build a line of data again
		line = ""
		for key in Keys:
			line += str(data_file[key][i]) + seperator
		#Output the line to console without the last seperator
		print(line[:-len(seperator)])

#Glue function that sticks all the helper functions together
def import_data(Target):
	#Target = "prelab.mt0"
	File_Target = open(Target)
	  
	Header = collect_header(File_Target)

	Col_Parts, Row_Count = determine_rows(Header)

	Data = parse_data(File_Target, Col_Parts, Row_Count)
	return Data

if __name__ == "__main__":
	
	if(len(sys.argv) <= 1):
		print("Usage:\tpython ckk5_prelab.py\t<FILE>\t<VAR1>\t<VAR2>\t<VAR3>\t<VAR4>")
		print("Variable arguments are optional. Omitting them outputs all data to console in csv format")
		print("Output is in CSV format seperated by \",\"")
	
	elif(len(sys.argv) <= 2):
		#If they're only two arguments, that means there's only a file given
		print_data(import_data(sys.argv[1]))
	else:
		#More than two items means they're keys expected
		print_data(import_data(sys.argv[1]), Keys = sys.argv[2:])
