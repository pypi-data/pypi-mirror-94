from setuptools import setup
from prisma_get_info.versions import APP_BUILD, APP_NAME, APP_VERSION

with open('README.md') as f:
    long_description = f.read()

setup(name="prisma_get_info",
      version="{0}-{1}".format(APP_VERSION, APP_BUILD),
      description='Utility to interact with Prisma via Panorama.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ebob9/prisma_get_info',
      author='Aaron Edwards',
      author_email='prisma_get_info@ebob9.com',
      license='MIT',
      install_requires=[
            'pan-python >= 0.16.0',
            'tabulate >= 0.8.7',
            'netaddr >= 0.8.0',
            'xmltodict >= 0.12.0'
      ],
      packages=['prisma_get_info'],
      entry_points={
            'console_scripts': [
                  'prisma_get_spn = prisma_get_info:go',
                  ]
      },
      classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
      ]
      )
