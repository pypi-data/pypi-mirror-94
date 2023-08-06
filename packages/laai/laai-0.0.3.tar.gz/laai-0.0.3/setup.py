from setuptools import setup

setup(
	name='laai',
	version='0.0.3',
	py_modules=['laai.main'],
	install_requires=['click', 'docker', 'mlflow'],
	extras_require={
        "optuna":  ["optuna", "sklearn", "plotly", "kaleido"],
    },
    include_package_data=True,
	entry_points='''
		[console_scripts]
		laai=laai.main:cli
	'''
)

