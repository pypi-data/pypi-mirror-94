from setuptools import setup, find_packages
setup(
    name='spider_lib',
    version='0.0.0.4',
    description='Spider',
    long_description="""Spider in python3 coroutine""",
    long_description_content_type="text/markdown",
    author='fubo',
    author_email='fb_linux@163.com',
    url='https://gitee.com/fubo_linux/spider',
    packages=find_packages(where='.', exclude=(), include=('*',)),
    package_data={
        "spider_lib": [
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'tqdm==4.56.0',
        'requests_async==0.6.2',
        'requests==2.25.1',
        'beautifulsoup4==4.9.3',
        'pydantic==1.7.3',
    ],
    python_requires='>=3.8'
)
