# Hypervoxelate: Hypervoxelation made easy!

Ever felt the need to cut up n-space into a bunch of tiny cubes and record the number of data points inside a cube _en masse_ using Python? Then hypervoxelate is the package for you!

## Rules of the package

Hypervoxelate takes in a 3D NumPy array ``data`` as input.  ``data`` consists of many n-dimensional _plots_, each with a fixed number of _data points_, and all data is plotted in a fixed number of _dimensions_.  The shape of the NumPy array should be (number of plots, number of data points, number of dimensions).  For each dimension, in order, specify any number of _cut points_.  These separate one hypervoxel from another along that dimension.  cut_points should be a list of lists, with the first list being the cut points along axis 0, and the last list being the cut points along the last axis.  The total number of hypervoxel counts return will be the product of the number of cut points along each dimension, across all dimensions.

Different cut points can be specified for each plot, enabling local mode, or the same cut points can be used for all plots, enabling global mode.  For local mode, input a 3D cut point array with one element (list) per combination of plot and dimension.  For global mode, input a 2D cut point array with one element (list) per dimension.

It is also possible to specify cut point selection via one of four pre-written algorithms.  If r is the resolution, then:
- Use ``cut_points="global_absolute"`` to separate each dimension along r-equally sized bins across all plots.
- Use ``cut_points="local_absolute"`` to separate each dimension along r-equally sized bins for _each_ plot; different plots will have different cut points.
- Use ``cut_points="global_relative"``to separate each dimension along the r-quantiles across all plots.
- Use ``cut_points="local_relative"`` to separate each dimension along the r-quantiles for _each_ plot.

Then use
```
from hypervoxelate import hypervoxelate

data = [[[0, 1], [1, 0], [2, 3], [3, 2]], [[0, 0], [1, 1], [2, 2], [3, 3]]]
cut_points = [[0.5, 1.5, 2.5], [1.5]]
plotted = hypervoxelate(data, cut_points=cut_points) # Global example

plotted = hypervoxelate(data, cut_points="local_relative", resolution=5) # Pre-specified
```

Other accessory methods from the function you might find useful include ``get_global_1D_data()``, which reshapes data in the form ``(num_points, dims)``, and the four cut point-specifying methods ``{global, local}_{relative, absolute}_cp()``.
