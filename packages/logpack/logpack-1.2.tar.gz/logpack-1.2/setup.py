import setuptools

setuptools.setup(
    name="logpack",
    version="1.2",
    author="Joxos",
    author_email="xujunhao61@163.com",
    description="Log for Python!",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/Joxos/logpack",
    packages=setuptools.find_packages(),
    install_requires=["datetime"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
