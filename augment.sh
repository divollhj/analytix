#!/bin/bash -e

if [ "$1" == "" ];then
echo "usage: $0 /path/to/anaconda"
exit
fi

PREFIX="$1"/bin
# yum -y install "gcc*" graphviz graphviz-devel "mesa-*" opencl-filesystem.noarch opencl-headers.noarch
export PATH="$PREFIX:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"
export LD_LIBRARY_PATH="$PREFIX/lib:/lib64:/usr/lib64:/usr/local/lib64:/lib:/usr/lib:/usr/local/lib"
export GEOS_DIR="$1"
# check certificates may comment the next 2 out
$PREFIX/conda update -n base conda -y
$PREFIX/conda config --set ssl_verify false
pcmd="$PREFIX/pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org"
$pcmd --upgrade pip
ccmd="$PREFIX/conda install -y"
#pcmd="$PREFIX/pip search --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org"
# pyopengl and numba in conflict?
$PREFIX/conda update --all -y
$ccmd R cartopy swig pyqtgraph traitlets vispy hdf4 pymssql boost cudatoolkit pyculib cmake line_profiler glib cython cairo
$pcmd msgpack argparse urwid
#$pcmd PyGObject
$pcmd construct hexdump sysv_ipc pypcapfile python-pcapng pyrasite pyrasite-gui pygraphviz avro spyder-memory-profiler veusz python-pptx orderedset PyOpenGL PyOpenGL-Demo PyOpenGL-accelerate objgraph
# python 3, pyrasite-gui and pygraphviz do not work, a dependency meliae does not appear to be python 3 compliant
# upgrading
#pcmd="$PREFIX/pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org -U"
#$pcmd msgpack argparse construct hexdump sysv_ipc pypcapfile python-pcapng pyrasite pyrasite-gui pygraphviz avro spyder-memory-profiler veusz python-pptx orderedset PyOpenGL PyOpenGL-Demo PyOpenGL-accelerate objgraph
#$pcmd pyopencl pycuda QScintilla
# done the below at work
#exit
tar -xf Downloads/ViTables-3.0.0.tar
cd ViTables-3.0.0
$PREFIX/python setup.py install
cd ..
rm -rf ViTables-3.0.0

unzip Downloads/cartopy-master.zip
cd cartopy-master
$PREFIX/python setup.py install
cd ..
rm -rf cartopy-master

tar -zxf Downloads/basemap-1.0.7.tar.gz
cd basemap-1.0.7
$PREFIX/python setup.py install
cd ..
rm -rf basemap-1.0.7

# version=$($PREFIX/python -V | awk '{print $1}'

mkdir -p $PREFIX/../lib/python2.7/site-packages/cartopy/data/shapefiles
cd $PREFIX/../lib/python2.7/site-packages/cartopy/data/shapefiles
tar -zxvf ~/natural_earth.tgz
cd -

mkdir -p $PREFIX/../lib/python2.7/site-packages/cartopy/data/raster/natural_earth
cp NE1_HR_LC_SR_W_DR.png $PREFIX/../lib/python2.7/site-packages/cartopy/data/raster/natural_earth/.

cd ~/Downloads
tar -jxvf p7zip_16.02_src_all.tar.bz2
cd p7zip_16.02
make
cp bin/7za $PREFIX/.
cd ..
rm -rf p7zip_16.02

exit
# working
tar -zxvf eric6-18.05.tar.gz
cd eric6-18.05
ins=$(dirname $PREFIX)
$PREFIX/python install.py -b $ins 
cd ..
rm -rf eric6-18.05