import setuptools


setuptools.setup(
    name="dict-to-object",
    version="1.0.3",
    license='MIT',
    author="oneofthezombies",
    author_email="hunhoekim@gmail.com",
    description="python dictionary to object.",
    long_description=open('README.md').read(),
    long_description_content_type = 'text/markdown',
    url="https://github.com/oneofthezombies/dict-to-object",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
