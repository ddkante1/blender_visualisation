## Info 
This code was used to render the Punctured Cell dataset as video and image in Blender. Each step of the dataset exists of red bloodcell and platelet objects. It's also split into a pre-set and the real simulation part.

Each frame required for the raw scientific data (XMF and HDF5) to be translated into the X3D file format. This was done with a [script](https://github.com/UvaCsl/HemoCell/tree/master/scripts/visualization) from the Hemocell github project. The data would be too large to be translated beforehand into X3D.

After, the 4 X3D files (RBC, PLT, PRE_RBC & PRE_PLT) are loaded into the Blender template. First the previous step is cleaned up. Then all objects are loaded in. Than a cleanup step is done.

This cleanup step is done to remove duplicate objects. The duplicate objects exist because of simulation parallelization reasons. This is done with the [removeDuplicates.py](https://github.com/ddkante1/blender_visualisation/blob/main/removeDuplicateObjects.py) Blender script. It first does some scaling, material assignment, etc. As the objects are in groups, it will split the objects in loose objects, set the origins of the objects to the center, than it will remove all objects closely sharing a origin position. The whole script is quite heavy, but especially this part is heavy and takes a long time to execute. Note that it looks for collections by name (RBC_Collection), materials by name (RBC_Mat), and also wants a reference to the folder where in the previous step the X3D files are stored.

Blender is closed and restarted but now doing the actual render.

## How To Run

Install the right Blender (for punctured cells it was version 2.8)

Prepare a Blender template file. This file will be loaded and used to render a frame.

Download Paraview:
```
curl 'https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.10&type=binary&os=Linux&downloadFile=ParaView-5.10.1-MPI-Linux-Python3.9-x86_64.tar.gz' --output ParaView-5.10.1-MPI-Linux-Python3.9-x86_64.tar.gz
```

Untar:
```
tar -xzvf ParaView-5.10.1-MPI-Linux-Python3.9-x86_64.tar.gz
```

Get git Hemocell project:

```
git clone https://github.com/UvaCsl/HemoCell.git
```

Set all paths in run_pipeline.sh

Set correct path in removeDuplicates.py

start:

```
./run_pipeline.sh
```

