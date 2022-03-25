"""
tracked_object.py defines TrackedObj -> a datatype which tracks on object methods
"""



import numpy as np
import operator
import functools
import copy 
import math
from collections.abc import Iterable
import uuid

def reset_array_prov(array, array_id = None):
    if array_id == None:
        array_id = uuid.uuid4()
    for index, x in np.ndenumerate(array):
        x.set_provenance(uuid.uuid4())
        x.write((array_id, array.shape, index))
    return array

def set_array_prov(array, fp, array_id = None):
    if array_id == None:
        array_id = uuid.uuid4()

    new_array = np.empty(array.shape, dtype=object)
    for index, x in np.ndenumerate(array):
        new_array[index] = TrackedObj(x, fp, uuid.uuid4())
        new_array[index].write((array_id, array.shape, index))
    return array


def add_provenance_copy(orig_func):
    #doesn't quite work when we return a data type that is not a float (works for a bit, but might not have
    # different functions)

    @functools.wraps(orig_func)
    def funct(ref, *args):
        args2 = []
        provenance = [ref.id]
        for arg in args:
            if hasattr(arg, 'id') and hasattr(arg, 'value'):
                provenance += arg.id
                args2.append(arg.value)
            else:
                args2.append(arg)
        args_size = len(args2)
        if args_size != 0:
            value = orig_func(ref,*args2)
        else:
            value = orig_func(ref)
            
        if not isinstance(value, Iterable):
            output = ref.__class__(value, ref.fp)
            for id in provenance:
                output.write(id)
        else:
            outputs = []
            for v in value:
                out = ref.__class__(v, ref.fp)
                outputs.append(out)
                for id in provenance:
                    out.write(id)
            output = tuple(outputs)
        return output
    return funct


class TrackedObj(object):
    """ Currently only supports float methods but can technically work for any data type
    """  
    
    def __init__(self, value, file_pointer, id = None):
        self.value = value
        if id == None:
            self.id = uuid.uuid4()
        else:
            self.id = id
        self.fp = file_pointer
    
    def write(self, prev, next = None):
        if next == None:
            next = self.id
        tup = str((prev, next))
        self.fp.write(tup)

    def set_provenance(self, id):
        self.id = id

    def set_value(self, value):
        self.value = value
    
    @add_provenance_copy
    def __abs__(self):
        return abs(self.value)

    @add_provenance_copy
    def __add__(self, other):
        return self.value + other
    
    @add_provenance_copy
    def __bool__(self):
        return bool(self.value)

    @add_provenance_copy
    def __divmod__(self, other):
        return divmod(self.value, other)
    
    @add_provenance_copy
    def __eq__(self, other):
        return self.value == other
    
    @add_provenance_copy
    def __float__(self):
        #TODO: We might want to change to datatype of the value without losing the provenance
        # How can we differentiate between the two cases?
        return float(self.value)

    @add_provenance_copy
    def __floordiv__(self, other):
        return self.value//other

    @add_provenance_copy
    def __ge__(self, other):
        return self.value >= other
    
    # def __format__(self, format_spec: str):
    #     return self.value.__format__(format_spec)

    # def __get_format__(self):
    #     return self.value.__getformat__()

    @add_provenance_copy
    def __gt__(self, other):
        return self.value > other

    @add_provenance_copy
    def __hash__(self):
        return hash(self.value)

    @add_provenance_copy
    def __le__(self, other):
        return self.value <= other

    @add_provenance_copy
    def __lt__(self, other):
        return self.value < other

    @add_provenance_copy
    def __mod__(self, other):
        return self.value % other

    @add_provenance_copy
    def __mul__(self, other):
        return self.value * other

    @add_provenance_copy
    def __ne__(self, other):
        return self.value != other
    
    @add_provenance_copy
    def __neg__(self):
        return -self.value

    @add_provenance_copy
    def __pos__(self):
        return +self.value
    
    @add_provenance_copy
    def __pow__(self, other):
        return self.value ** other

    @add_provenance_copy
    def __radd__(self, other):
        return other + self.value

    @add_provenance_copy
    def __rdivmod__(self, other):
        return divmod(other, self.value)
    
    #TODO: __reduce__ __reduce_ex__ function not defined?

    @add_provenance_copy
    def __rfloordiv__(self, other):
        return other //self.value

    @add_provenance_copy
    def __rmod__(self, other):
        return other % self.value

    @add_provenance_copy
    def __rmul__(self, other):
        return other * self.value
    
    @add_provenance_copy
    def __round__(self):
        return round(self.value)

    @add_provenance_copy
    def __rpow__(self, other):
        return other ** self.value

    @add_provenance_copy
    def __rsub__(self, other):
        return other - self.value

    @add_provenance_copy
    def __rtruediv__(self, other):
        return other / self.value
    
    #def __setformat__
    
    @add_provenance_copy
    def __sub__(self, other):
        return self.value - other

    @add_provenance_copy
    def __truediv__(self, other):
        return self.value/other

    @add_provenance_copy
    def __trunc__(self):
        return math.trunc(self.value)

    @add_provenance_copy
    def as_integer_ratio(self):
        return self.value.as_integer_ratio()

    @add_provenance_copy
    def conjugate(self):
        return self.value.conjugate()

    # def from_hex
    @add_provenance_copy
    def hex(self):
        return self.value.hex()

    @add_provenance_copy
    def imag(self):
        return self.value.imag()

    @add_provenance_copy
    def is_integer(self):
        return self.value.is_integer()    

    @add_provenance_copy
    def real(self):
        return self.value.real()

        
    def __str__(self):
        return str((self.value, self.provenance))
    
    def __repr__(self):
        return str((self.value, self.provenance))

# why get and set? -> set might make sense

# arr = np.empty((3, 1), dtype=object)
# arr[0] = TrackedObj(0, None)
# arr[1] = TrackedObj(5, None)
# arr[2] = TrackedObj(8, None)
# reset_array_prov(arr)
# print(arr.sum().provenance)
# save_array_prov(arr, './logs')

# x = TrackedObj(10.10, 1)
# import math

# print(math.trunc(x))