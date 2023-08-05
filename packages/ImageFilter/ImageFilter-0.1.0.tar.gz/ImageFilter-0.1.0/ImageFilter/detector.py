from PIL import Image

# YCbCr Reference:
# http://www.naun.org/multimedia/NAUN/computers/20-462.pdf

def process_image(image_path):
	image = Image.open(image_path)

	if image.mode != 'YCbCr':
		image = image.convert('YCbCr')
	return image

def predict(image, threshold=0.2):
	ycbcr_data = image.getdata()
	width, height = image.size
	skin_pixel_count = 0

	for i, data in enumerate(ycbcr_data):
		y, cb, cr = data
		if 80 <= cb <= 127 and 130 <= cr <= 168:
			skin_pixel_count += 1

	if skin_pixel_count > threshold * width * height:
		return True
	else:
		return False

def main():
	import sys, os
	argv = sys.argv[1:]
	images = list()

	try:
		if argv[0]:
			if os.path.isdir(argv[0]):
				print(f"[*] Analysing {argv[0]}")
				from glob import glob
				for image_extension in ['png', 'jpg']:
					images += glob(argv[0] + '*.{}'.format(image_extension))

				for file_path in images:
					processed_image = process_image(file_path)
					predicted = predict(processed_image)
					print(f"{file_path[len(argv[0]) - 1:] if len(file_path) > 15 else file_path}: {predicted}" + \
						' ' * 40, end='\r' if '-v' not in argv else '\n')
					if '-ar' in argv and predicted:
						print(f"[i] Removing: {file_path}")
						os.remove(file_path)
		else:
			print("USAGE:")
			print("imagefilter <directory> [-r][-ar][-v]")
			print("")
			#print("-r  -- Recursive scan")
			print("-ar -- Auto remove detected files (dangerous)")
			print("-v  -- Verbose output (good for debug)")
	except IndexError:
		print("USAGE:")
		print("imagefilter <directory> [-r][-ar][-v]")
		print("")
		#print("-r  -- Recursive scan")
		print("-ar -- Auto remove detected files (dangerous)")
		print("-v  -- Verbose output (good for debug)")

if __name__ == '__main__':
	main()
