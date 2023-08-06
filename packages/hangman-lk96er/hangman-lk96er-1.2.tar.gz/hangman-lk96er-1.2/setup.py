import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
   name='hangman-lk96er',
   version='1.2',
   description='A simple hangman game I created. Language: German',
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="",
   author='Lucas',
   author_email='not_areale@mail.com',
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
   packages=setuptools.find_packages(),
   python_requires='>=3.6',
)
