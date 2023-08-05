import setuptools

with open("README.md", 'r', encoding='utf-8') as f:
	description = f.read()

setuptools.setup(
	name="ImageFilter",
	version="0.1.0",
	author="HanzHaxors",
	author_email="hanzhaxors@gmail.com",
	description="We can't vaporize porn but we can reduce porn, and we only helps it.",
	long_description=description,
	long_description_content_type='text/markdown',
	url="https://github.com/HanzHaxors/PornFreeKit",
	packages=["ImageFilter"],
	entry_points={
		"console_scripts": [
			"imagefilter = ImageFilter.detector:main"
		]
	},
	classifiers=[
		"Topic :: Scientific/Engineering :: Image Processing",
		"Topic :: Scientific/Engineering :: Image Recognition"
	],
	install_requires=[
		"Pillow>=8.1.0"
	],
	python_requires=">=3.6"
)
