# Testing igl's implementation of LBO for use on the cortical surface

This is a small module containing functions which makes it easy to test the effectiveness of the Laplace-Beltrami Operator in libigl on the cortical surface.

## Installation

It is recommended that you install this in its own conda environment. igl and meshplot must be installed via conda. It is recommended you follow the steps below:

```
conda create --name igl_env -c conda-forge igl meshplot
conda activate igl_env
git clone https://github.com/jackt3/igl_testing.git
cd igl_testing
python -m pip install -U .
```

As well as igl and meshplot, the module also has several other requirements, including numpy, scipy and nibabel.

If this is to be installed alongside Toblerone (or another module requiring Python 3.7) please use the adjusted command below to create your conda environment:

```
conda create --name igl_env -c conda-forge python=3.7 igl meshplot
```

## Usage

The module has a list of functions implemented (although it's currently a list of 1) and offers a command-line interface as shown below. Given a surface mesh, it will evaluate the desired function on the co-ordinates of the vertices. It then calculates both the Laplace-Beltrami Operator and, if desired for comparison, the Graph Laplacian of the surface. The evaluation of the function, as well as the curvature as calculated by these operators, are then saved to the filenames provided.

An example of using the command-line interface can be found below:

```
lap_of_func <surface_name> <function_savename> <lbo_u_savename>
```

If desired, the function can be specified via the -f flag, although currently only one function has been implemented (sum of sine and cosine):

```
lap_of_func <surface_name> <function_savename> <lbo_u_savename> -f <function>
```

If you want to generate the result using the graph Laplacian for comparison, just add a savename for the result:

```
lap_of_func <surface_name> <function_savename> <lbo_u_savename> --glu_name=<gl_u_savename>
```