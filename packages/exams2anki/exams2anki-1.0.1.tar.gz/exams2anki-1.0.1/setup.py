from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='exams2anki',
    version='1.0.1',
    author='Guilherme Caulada',
    author_email='guilherme.caulada@gmail.com',
    url='https://github.com/Sighmir/exams2anki',
    description='Convert ExamTopics pages to Anki decks!',
    license='AGPL-3.0',
    packages=find_packages(),
    entry_points={
            'console_scripts': [
                'gfg = src.exams2anki:main'
            ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ),
    keywords='anki examtopics exam certification cert sighmir',
    install_requires=requirements,
    zip_safe=False
)
