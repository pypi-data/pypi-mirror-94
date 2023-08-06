import setuptools


with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='cv_stream',
    version='0.1.0',
    author='Brennen Herbruck',
    author_email='brennen.hrbruck@gmail.com',
    description='Remote OpenCV development server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bherbruck/cv_stream',
    packages=['cv_stream'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    python_requires='>=3.6',
)