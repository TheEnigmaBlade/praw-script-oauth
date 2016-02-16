import os

def read_config(config_file, config_dir="."):
	path = os.path.join(config_dir, config_file)
	try:
		with open(path, "r") as f:
			token = f.readline()
			time = int(f.readline())
			return token, time
	except FileNotFoundError:
		return None, 0

def write_config(token, time, config_file, config_dir="."):
	path = os.path.join(config_dir, config_file)
	with open(path, "w") as f:
		f.write(str(token)+"\n")
		f.write(str(time))
