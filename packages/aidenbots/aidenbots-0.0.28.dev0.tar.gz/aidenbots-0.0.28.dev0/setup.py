import setuptools

setuptools.setup(
    name="aidenbots",
    version="0.0.28-dev",
    author="Per Aspera Adastra",
    author_email="adastra.aspera.per@gmail.com",
    include_package_data=True,
    description="Opentrons automated protocols developed in the Aiden Lab",
    url="https://github.com/aidenlab/ot2-bots",
    packages=setuptools.find_packages(),
    # packages=setuptools.find_packages(exclude=["aidenbots.bin", "aidenbots.protocols"]),
    package_data={'': ['sounds/Bb_A_Bb_pause.mp3']},
    install_requires=[
        'opentrons >= 3.21.2',
    ],
    entry_points={
        'console_scripts': [
            'aidenbots_check = aidenbots.check:main',
        ],
    },
    python_requires='>=3.7',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
