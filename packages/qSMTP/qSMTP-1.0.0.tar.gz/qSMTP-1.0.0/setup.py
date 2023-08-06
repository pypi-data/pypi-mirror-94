from distutils.core import setup
from setuptools import setup, find_packages
setup(
    name = 'qSMTP',
    version = '1.0.0',
    keywords = ('SMTP', 'quickly STMP'),
    description = 'private module for quickly sending mail to others',
    license = 'MIT License',
    author = 'zwy',
    python_require=">=3.2",
    # install_requires=['oss2','tqdm'],
    author_email = 'zuowangyang@foxmail.com',
    packages = find_packages("src"),# 需要打包的package,使用find_packages 来动态获取package，exclude参数的存在，使打包的时候，排除掉这些文件
    platforms = 'any',
    package_dir={"":"src"},
    include_package_data = True,
)