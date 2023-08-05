from setuptools import setup

setup(
    name='nvidia-smi-hide',
    version='0.12',
    author='meepo',
    py_modules=['nvidia_smi_hide'],
    install_requires=[
        'pynvml==8.0.4',
    ],
    # python modules name support "_" not "-"
    # but you still can leave "nvidia-smi-hide" as your binary name
    entry_points='''
        [console_scripts]
        nvidia-smi-hide=nvidia_smi_hide:main
    ''',
)
