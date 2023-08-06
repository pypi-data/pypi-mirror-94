import setuptools

setuptools.setup(
    name="dict-to-object",
    version="1.0.0",
    license='MIT',
    author="oneofthezombies",
    author_email="hunhoekim@gmail.com",
    description="dictionary to object.",
    long_description=open('README.md').read(),
    url="https://github.com/oneofthezombies/dict-to-object",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)