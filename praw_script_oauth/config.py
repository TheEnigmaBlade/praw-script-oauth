import os

def read_config(config_file, config_dir="."):
	path = os.path.join(config_dir, config_file)
	try:
		with open(path, "r") as f:
			token = f.readline().strip()
			time = int(f.readline().strip())
			return token, time
	except (FileNotFoundError, ValueError):
		return None, 0

def write_config(token, time, config_file, config_dir="."):
	if token is not None:
		path = os.path.join(config_dir, config_file)
		with open(path, "w") as f:
			f.write(str(token)+"\n")
			f.write(str(time))
