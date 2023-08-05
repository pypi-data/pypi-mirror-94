from setuptools import setup, find_packages
setup(
    name='evolution_strategy',
    version='0.0.0.1',
    description='Evolution Strategy',
    long_description="""Evolution Strategy""",
    long_description_content_type="text/markdown",
    author='fubo',
    author_email='fb_linux@163.com',
    url='https://gitee.com/fubo_linux/spider',
    packages=find_packages(where='.', exclude=(), include=('*',)),
    package_data={
        "evolution_strategy": [
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'tqdm==4.56.0',
        'pydantic==1.7.3',
        'tensorboardX==2.1'
    ],
    python_requires='>=3.8'
)
