from setuptools import setup, find_packages


setup(
    name='flowroute-messaging-fossum',
    version='0.1.0',
    license='MIT',
    description='Flowroute\'s Messaging API (Fossum edition).',
    author='Flowroute Developers',
    author_email='fossum.eric@gmail.com',
    url='https://github.com/fossum/flowroute-messaging-python',
    packages=find_packages('.'),
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Telephony'
    ],
    keywords=[
        'messaging', 'sms', 'telephony', 'sip', 'api'
    ],
    install_requires=[
        'requests',
        'jsonpickle',
    ],
)
