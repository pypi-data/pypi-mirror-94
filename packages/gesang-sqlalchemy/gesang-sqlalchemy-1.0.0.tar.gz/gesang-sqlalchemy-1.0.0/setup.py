from setuptools import setup, find_packages

setup(
    name="gesang-sqlalchemy",
    version="1.0.0",
    description="A sql orm framework based on sqlalchemy for gesang api framework.",
    author="Dong Zhang",
    author_email="785576549@qq.com",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "sqlalchemy",
        "gesang"
    ],
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False
)
