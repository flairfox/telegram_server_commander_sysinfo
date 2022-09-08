import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sysinfo",
    version="0.0.1",
    author="flairfox",
    description="Sysinfo module for Telegram Server Commander Bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flairfox/telegram_server_commander_sysinfo",
    packages=setuptools.find_packages(),
    install_requires=['psutil', 'flask'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
