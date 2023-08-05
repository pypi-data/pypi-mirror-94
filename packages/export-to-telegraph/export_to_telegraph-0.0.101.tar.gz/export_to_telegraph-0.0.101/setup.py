import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="export_to_telegraph",
    version="0.0.101",
    author="Yunzhi Gao",
    author_email="gaoyunzhi@gmail.com",
    description="Library for export webpage to Telegraph.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaoyunzhi/export_to_telegraph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'html_telegraph_poster',
        'bs4',
        'readability-lxml',
        'telegram_util',
        'readee',
        'opencc-python-reimplemented',
        'cached_url',
        'weibo_2_album',
        'gphoto_2_album',
    ],
    python_requires='>=3.0',
)