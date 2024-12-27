def array_to_indices(arr, index):
    return tuple(index[i] for i in arr)

def dict_to_array(source, keys):
    return [source.get(k, None) for k in keys]
