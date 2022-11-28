import struct

def unpackDataBytes(data):
		size_of_int = 4
		size_of_char = 1
		size_of_float = 4

		# compute amount of int data
		n_int = 4
		n_int_str = 'i'*n_int #'iiii'

		# compute amount of char data
		n_char = 2
		n_char_str = 'c'*n_char #'cc'

		# compute amount of float data
		n_float = int(len(data) - n_int*size_of_int - n_char*size_of_char) # extract metadata. Last char is \n
		n_float = int(n_float/size_of_float)
		n_float_str = 'f'*n_float

		values_tuple = struct.unpack(n_float_str + n_int_str + n_char_str, data) #returns tuple

		mean_time = values_tuple[-6] #microseconds
		mean_time_total = values_tuple[-5] #microseconds
		angle = values_tuple[-4]
		steps_to_move = values_tuple[-3]
		direction_char = str(values_tuple[-2],'utf-8')
		float_tuple = values_tuple[0:-6]  #remove last elements
		float_list = list(float_tuple)

		return angle, direction_char, float_list, mean_time, mean_time_total

data = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00r\n'

angle, direction_char, float_list, _, mean_time_total = unpackDataBytes(data)
print(angle, direction_char, float_list, mean_time_total)