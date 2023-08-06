import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='thaibulksms_api',
    version='1.0.7',
    description='Thaibulksms API for send sms',
    author='thaibulksms_api',
    author_email='apichart@1moby.com',
    packages=['thaibulksms_api'],
    license="thaibulksms",
    #   url='https://github.com/morangesolution/bahttext',
    #   download_url='https://github.com/morangesolution/bahttext/tarball/master',
)
