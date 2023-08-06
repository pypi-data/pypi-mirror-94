from distutils.core import setup
from setuptools import setup, find_packages
setup(
    name = 'qalioss',
    version = '0.0.1',
    keywords = ('alioss', 'aliyun'),
    description = 'self module for quickly uploading or downloading folders from ali oss',
    license = 'MIT License',
    author = 'zwy',
    python_require=">=3.5",
    install_requires=['oss2','tqdm'],
    author_email = 'zuowangyang@foxmail.com',
    packages = find_packages("src",exclude=['build']),# 需要打包的package,使用find_packages 来动态获取package，exclude参数的存在，使打包的时候，排除掉这些文件
    platforms = 'any',
)