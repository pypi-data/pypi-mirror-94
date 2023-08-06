import setuptools


setuptools.setup(name='webscrapingjordi',
      version="1.0.0",
      url = "https://github.com/jordicam/web-scraping", 
      description='Download images and paragraphs from a webpage',
      author='Jordi Camacho',
      author_email='jordicamacho88@gmail.com',
      packages=setuptools.find_packages(),
      install_requires=["requests","bs4","pandas"],
      classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
       ],
     )