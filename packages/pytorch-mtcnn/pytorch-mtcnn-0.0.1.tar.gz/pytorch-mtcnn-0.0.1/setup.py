import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='pytorch-mtcnn',
    version='0.0.1',
    author='David Mosallanezhad',
    author_email='amosalla@asu.edu',
    description='MTCNN using Pytorch.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Davood-M/mtcnn-pytorch",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'torch', 'Pillow', 'opencv_python'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
