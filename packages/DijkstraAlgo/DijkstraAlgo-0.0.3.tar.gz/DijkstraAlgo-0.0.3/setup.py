from setuptools import setup

with open("ReadMe.md", 'r', encoding="utf-8") as file:
    long_description = file.read()

setup(
    name= 'DijkstraAlgo',
    version= '0.0.3',
    description= '''To measure the shortest distance of any nodes or any particular points, we can use this package.
    By using this package, we will get the shortest path and also the distance.''',
    py_modules=["DijkstraAlgo"],
    package_dir={'': 'src'},
    author= "Md Mizanur Rahman Mustakim",
    author_email= 'mustakim.mizan@gmail.com',
    url= 'https://github.com/MizanMustakim/Dijkstra-s-Shortest-Path-Algorithm',
    download_url= 'https://github.com/MizanMustakim/Dijkstra-s-Shortest-Path-Algorithm/archive/0.0.1.tar.gz',
    keywords= ['Shortest Path', 'Dijkstra Algorithm', 'Graph', 'Shortest Distance', 'Shortest Route', 'Dijkstra_2D', 'Dijkstra_3D'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers= [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    extras_require= {
        "dev": [
            "pytest>=3.7",
        ],
    },
)