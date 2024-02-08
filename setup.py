from setuptools import setup, find_packages


install_requires = [
    "boto3 ~= 1.26.151",
    "botocore ~= 1.29.151",
    "celery ~= 5.2.7",
    "celery[sqs] ~= 5.2.3",
    "django ~= 4.2.9",
    "django-cors-headers ~= 3.13.0",
    "django_celery_beat ~= 2.5.0",
    "django_celery_results ~= 2.4.0",
    "django-extensions ~= 3.2.1",
    "djangorestframework ~= 3.14.0",
    # "djangorestframework-simplejwt ~= 5.2.1",
    "psycopg2-binary ~= 2.9.3",
    "python-decouple ~= 3.6",
    "requests ~= 2.28.1",
]

tests_require = [
    "pytest",
    "pytest-django",
    "pytest-cov",
    "pytest-freezegun",
    "pytest-mock",
    "pytest-celery",
    "pytest-check",
    "moto[s3]"
]

setup(
    name="commuter_rail_departure",
    version="0.1.4",
    description="Commuter Rail Departure",
    author="Zach Cook",
    author_email="zach@web3technologies.io",
    install_requires=install_requires,
    include_package_data=True,
    packages=find_packages("src"),
    test_suite="tests",
    tests_require=tests_require,
    extras_require={
        "test": tests_require,
    },
    package_dir={"":"src"},
    )