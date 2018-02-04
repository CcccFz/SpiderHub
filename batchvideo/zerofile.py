import os


base_path = os.path.dirname(__file__)
for curdir, dirnames, filenames in os.walk('videos'):
	dir_path = os.path.join(base_path, curdir)
	for filename in filenames:
		file_path = os.path.join(dir_path, filename)
		if os.path.getsize(file_path) == 0:
			print(file_path)
			os.remove(file_path)