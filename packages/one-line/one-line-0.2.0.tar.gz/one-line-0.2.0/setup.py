import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='one-line',
    version='0.2.0',
    description='Make every step oneLine.',
    long_description=long_description,  # 没有 README 这一项可以不要
    long_description_content_type="text/markdown",
    install_requires=[  # 该包的依赖包，安装时会检查是否满足依赖要求
        'pandas',
        'seaborn',
        'scipy',
        'scikit-learn'
    ],
    packages=setuptools.find_packages(),  # 该库中含有的包，一般就自动搜索
    author='Zeesain Tsui',
    author_email='clarenceehsu@163.com',
    url='https://github.com/clarenceehsu/oneLine',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)