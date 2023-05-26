import setuptools

setuptools.setup(
      name='fscraper',
      version='1.0.0',
      description='Financial Data Web Scraper',
      author='er-ri',
      author_email='724chen@gmail.com',
      url='https://github.com/er-ri/fscraper',
      packages=['fscraper'],
      classifiers=[
            "Programming Language :: Python :: 3.10",
            "License :: OSI Approved :: MIT License",
      ], 
      python_requires='>=3.8',
      install_requires=[
            'pandas',
            'numpy',
            'requests',
      ],
)