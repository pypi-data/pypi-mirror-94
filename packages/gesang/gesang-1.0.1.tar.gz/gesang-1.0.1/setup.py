from setuptools import setup, find_packages


filepath = "readme.md"


setup(
    name="gesang",
    version="1.0.1",
    description="A restful api framework with starlette.",
    long_description=open(filepath, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author="Dong Zhang",
    author_email="785576549@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    entry_points={
        "console_scripts": [
            "gesang-admin = gesang.bin.entry:execute_from_argv",
        ]
    },
    install_requires=[
        "starlette",
        "uvicorn",
        "python-multipart",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False
)
