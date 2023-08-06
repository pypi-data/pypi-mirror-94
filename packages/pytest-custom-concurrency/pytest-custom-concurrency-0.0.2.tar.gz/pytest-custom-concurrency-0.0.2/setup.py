from setuptools import setup

"""
author: fungaegis
github: https://github.com/fungaegis/pytest_custom_Concurrency
"""

setup(
    name='pytest-custom-concurrency',
    url='https://github.com/fungaegis/pytest-custom-concurrency',
    version='0.0.2',
    author="fungaegis",
    author_email="fungaegis@gmail.com",
    description='Custom grouping concurrence for pytest',
    long_description='Custom grouping concurrence for pytest;\n'
                     ' Usage: cmd line or main function --group=group_name --concurrent=on',
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.7',
    ],
    license='MIT License',
    py_modules=['pytest_custom_concurrency'],
    keywords=[
        'pytest', 'py.test', 'pytest_custom_concurrency', 'concurrency'
    ],

    install_requires=[
        'pytest'
    ],
    entry_points={
        'pytest11': [
            'custom_concurrency = pytest_custom_concurrency',
        ]
    }
)
