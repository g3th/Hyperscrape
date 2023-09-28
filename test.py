import os
from pathlib import Path
stuff = ['one', 'two' , 'three']


for link, index in enumerate(stuff):
    print(index[link])
    if link == 1:
        link = 0