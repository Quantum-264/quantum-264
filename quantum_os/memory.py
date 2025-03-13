import gc
def get_free_memory(full=False):
    gc.collect()
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F+A
    P = 'MEM USAGE {0:.2f}%'.format(100-(F/T*100))
    return {'total':T,'free':F,'used':A,'percent':P}
    

