import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sp-api-clients",  # Replace with your own username
    version="0.2.5",
    author="Haoyu Pan",
    author_email="panhaoyu.china@outlook.com",
    description="Amazon selling partner api clients.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/panhaoyu/sp-api-clients",
    packages=['sp_api_clients'],
    install_requires=[
        'peewee',
        'cachetools',
        'requests',
        'boto3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
