def index_of(it, f, default_index=-1):
    return next((i for i, e in enumerate(it) if f(e)), default_index)
