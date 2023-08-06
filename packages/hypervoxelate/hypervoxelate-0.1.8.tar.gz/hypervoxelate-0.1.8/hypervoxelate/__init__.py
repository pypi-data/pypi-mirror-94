import numpy as np
import warnings

def global_absolute_cp(data, resolution):
    NUM_PLOTS = np.size(data, axis=0)
    NUM_POINTS = np.size(data, axis=1)
    NUM_DIMS = np.size(data, axis=2)

    flat_data = get_global_1D_data(data)
    cut_points = []
    if isinstance(resolution, (int)):
        min = np.amin(flat_data, axis=0)
        max = np.amax(flat_data, axis=0)

        multiplier = np.array(range(1, resolution))
        multiplier = multiplier / resolution
        multiplier = np.reshape(multiplier, (-1, 1))
        multiplier = np.repeat(multiplier, NUM_DIMS, axis=1)

        cut_points = multiplier * (max - min)
        cut_points = cut_points + min
        cut_points = np.swapaxes(cut_points, 0, 1)
    else:
        for dim in range(0, NUM_DIMS):
            slice_flat_data = np.reshape(flat_data[:, dim], (1, np.size(flat_data, axis=0), np.size(flat_data, axis=1)))
            cut_points.append(global_absolute_cp(slice_flat_data, resolution[dim])[0, :])
    return cut_points

def local_absolute_cp(data, resolution):
    NUM_PLOTS = np.size(data, axis=0)
    NUM_POINTS = np.size(data, axis=1)
    NUM_DIMS = np.size(data, axis=2)

    cut_points = []
    for plot in range(0, NUM_PLOTS):
        data_slice = data[plot, :, :]
        data_slice = np.reshape(data_slice, (1, np.size(data_slice, axis=0), 1))
        cut_points.append(global_absolute_cp(data_slice, resolution))
    return cut_points

def global_relative_cp(data, resolution):
    NUM_PLOTS = np.size(data, axis=0)
    NUM_POINTS = np.size(data, axis=1)
    NUM_DIMS = np.size(data, axis=2)

    flat_data = get_global_1D_data(data)
    cut_points = []
    if isinstance(resolution, (int)):
        quantile_cuts = np.array(range(1, resolution)) / resolution
        cut_points = np.swapaxes(np.quantile(flat_data, quantile_cuts, axis=0), 0, 1)
    else:
        for dim in range(0, NUM_DIMS):
            slice_flat_data = np.reshape(flat_data[:, dim], (1, np.size(flat_data, axis=0), 1))
            cut_points.append(global_relative_cp(slice_flat_data, resolution[dim])[0, :])
    return cut_points

def local_relative_cp(data, resolution):
    NUM_PLOTS = np.size(data, axis=0)
    NUM_POINTS = np.size(data, axis=1)
    NUM_DIMS = np.size(data, axis=2)

    cut_points = []
    for plot in range(0, NUM_PLOTS):
        data_slice = data[plot, :, :]
        data_slice = np.reshape(data_slice, (1, np.size(data_slice, axis=0), np.size(data_slice, axis=1)))
        cut_points.append(global_relative_cp(data_slice, resolution))

    return cut_points

def get_global_1D_data(data):
    # Basic data checks
    if not isinstance(data, (np.ndarray)):
        raise TypeError("Data input was not a NumPy array")
    if data.ndim != 3:
        raise TypeError("Data is not 3D (plots, points, dims)")

    # Return
    data = np.reshape(data, (np.size(data, axis=0) * np.size(data, axis=1), -1))
    return data

def reverse_axes_except_first(data):
    for lower_axis in range(1, data.ndim // 2 + 1):
        data = np.swapaxes(data, lower_axis, data.ndim - lower_axis)
    return data

def hypervoxelate(data, cut_points="global_absolute", side="left", resolution=-1):
    NUM_PLOTS = np.size(data, axis=0)
    NUM_POINTS = np.size(data, axis=1)
    NUM_DIMS = np.size(data, axis=2)

    # Default cut point modes
    if isinstance(cut_points, (str)):
        if resolution == -1:
            raise ValueError("cut_points was specified via string, but resolution was not specified.  Make sure resolution is set to a positive integer")
        if cut_points == "global_absolute":
            cut_points = global_absolute_cp(data, resolution)
        elif cut_points == "local_absolute":
            cut_points = local_absolute_cp(data, resolution)
        elif cut_points == "global_relative":
            cut_points = global_relative_cp(data, resolution)
        elif cut_points == "local_relative":
            cut_points = local_relative_cp(data, resolution)
        else:
            raise ValueError("cut_points is not specified via a valid string.  The only valid strings are global_absolute, local_absolute, global_relative, and local_relative")
    elif isinstance(cut_points, (np.ndarray, list)):
        if resolution != -1:
            warnings.warn("A resolution has been specified but will not be used, because cut_points was passed via array not string")
    else:
        raise TypeError("Cut points were not passed as an array")

    if isinstance(cut_points, (np.ndarray)):
        cut_points = cut_points.tolist()

    # Basic data checks
    if not isinstance(data, (np.ndarray)):
        raise TypeError("Data was not passed as a NumPy array")
    if len(np.shape(data)) != 3:
        raise TypeError("Data to be hypervoxelated is not 3D (plots, points, dims)")
    if side != "left" and side != "right":
        raise ValueError("side is neither left nor right")

    # Get mode (global/local)
    mode = "local"
    if isinstance(cut_points[0][0], (int, float)):
        mode = "global"
    else:
        cut_num_example = []
        for dim in range(0, NUM_DIMS):
            cut_num_example.append(len(cut_points[0][dim]))
        for plot in range(0, NUM_PLOTS):
            for dim in range(0, NUM_DIMS):
                if cut_num_example[dim] != len(cut_points[plot][dim]):
                    raise ValueError("In local mode, not all cut point arrays are of the same size across plots")

    # Convert data from values to bin rankings
    for plot_index in range(0, np.size(data, axis=0)):
        for dim_index in range(0, np.size(data, axis=2)):
            if mode == "local":
                data[plot_index, :, dim_index] = np.searchsorted(cut_points[plot_index][dim_index], data[plot_index, :, dim_index], side=side)
            else:
                data[plot_index, :, dim_index] = np.searchsorted(cut_points[dim_index], data[plot_index, :, dim_index], side=side)

    # Replace each data point's numdims tuple with a single number
    flattened = np.zeros((NUM_PLOTS, NUM_POINTS))

    partial_products = []
    partial_product = 1
    for new_dim in range(0, NUM_DIMS + 1):
        partial_products.append(partial_product)
        if new_dim != NUM_DIMS:
            if mode == "local":
                partial_product = partial_product * (len(cut_points[0][new_dim]) + 1)
            else:
                partial_product = partial_product * (len(cut_points[new_dim]) + 1)

    for dim in range(0, NUM_DIMS):
        flattened = flattened + partial_products[dim] * data[:, :, dim]
    flattened = flattened.astype('int64')

    # Plots points in hyperspace
    shape_arr = []
    for dim in range(0, NUM_DIMS):
        if mode == "local":
            shape_arr.append(len(cut_points[0][dim]) + 1)
        else:
            shape_arr.append(len(cut_points[dim]) + 1)
    shape_arr = [x for x in reversed(shape_arr)]

    hyper = []
    for plot in range(0, NUM_PLOTS):
        hyper.append(np.reshape(np.bincount(flattened[plot, :], minlength=partial_products[-1]), shape_arr))
    hyper = np.array(hyper)
    hyper = reverse_axes_except_first(hyper)

    return hyper
