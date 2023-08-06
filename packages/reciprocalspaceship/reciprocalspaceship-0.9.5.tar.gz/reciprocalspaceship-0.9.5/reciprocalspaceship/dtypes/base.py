import numpy as np
from pandas.core import nanops
from pandas.core.indexers import check_array_indexer
from pandas.core.construction import extract_array
from pandas._libs import lib, missing as libmissing
from pandas.api.extensions import (
    ExtensionDtype,
    ExtensionArray,
    ExtensionScalarOpsMixin,
    take
)
from pandas.core.arrays.integer import IntegerArray, coerce_to_array
from pandas.core.tools.numeric import to_numeric
from pandas.util._decorators import cache_readonly
from pandas.core.dtypes.cast import astype_nansafe
from pandas.core.dtypes.common import is_dtype_equal
import pandas as pd

class MTZDtype(ExtensionDtype):
    """Base ExtensionDtype for implementing persistent MTZ data types"""

    @classmethod
    def construct_from_string(cls, string):
        if not isinstance(string, str):
            raise TypeError(f"'construct_from_string' expects a string, got {type(string)}")
        elif string != cls.name and string != cls.mtztype:
            raise TypeError(f"Cannot construct a '{cls.__name__}' from '{string}'")
        return cls()

class MTZInt32Dtype(MTZDtype, pd.Int32Dtype):
    """Base ExtensionDtype class for MTZDtype backed by pd.Int32Dtype"""

    def _get_common_dtype(self, dtypes):
        if len(set(dtypes)) == 1:
            # only itself
            return self
        else:
            return super(pd.Int32Dtype, self)._get_common_dtype(dtypes)
    
    def __repr__(self):
        return self.name

class MTZIntegerArray(IntegerArray):

    @cache_readonly
    def dtype(self):
        return self._dtype

    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        values, mask = coerce_to_array(scalars, dtype=dtype, copy=copy)
        return cls(values, mask)

    @classmethod
    def _from_factorized(cls, values, original):
        values, mask = coerce_to_array(values, dtype=original.dtype)
        return cls(values, mask)

    def reshape(self, *args, **kwargs):
        return self._data.reshape(*args, **kwargs)

    def to_numpy(self, dtype=None, copy=False, na_value=lib.no_default):
        """
        Convert to a NumPy Array.

        If array does not contain any NaN values, will return a np.int32
        ndarray. If array contains NaN values, will return a ndarray of 
        object dtype.

        Parameters
        ----------
        dtype : dtype, default np.int32 or np.float32
            The numpy dtype to return
        copy : bool, default False
            Whether to ensure that the returned value is a not a view on
            the array. Note that ``copy=False`` does not *ensure* that
            ``to_numpy()`` is no-copy. Rather, ``copy=True`` ensure that
            a copy is made, even if not strictly necessary. This is typically
            only possible when no missing values are present and `dtype`
            is the equivalent numpy dtype.
        na_value : scalar, optional
             Scalar missing value indicator to use in numpy array. Defaults
             to the native missing value indicator of this array.

        Returns
        -------
        numpy.ndarray
        """
        if na_value is lib.no_default:
            na_value = libmissing.NA

        if dtype is None:
            if self._hasna:
                dtype = object
            else:
                dtype = np.int32

        if self._hasna:
            data = self._data.astype(dtype, copy=copy)
            data[self._mask] = na_value
        else:
            data = self._data.astype(dtype, copy=copy)

        return data

    def value_counts(self, dropna=True):
        """
        Returns a DataSeries containing counts of each category.
        Every category will have an entry, even those with a count of 0.

        Parameters
        ----------
        dropna : bool, default True
            Don't include counts of NaN.

        Returns
        -------
        counts : DataSeries
        """
        from pandas import Index
        import reciprocalspaceship as rs

        # compute counts on the data with no nans
        data = self._data[~self._mask]
        value_counts = Index(data).value_counts()
        array = value_counts.values

        # TODO(extension)
        # if we have allow Index to hold an ExtensionArray
        # this is easier
        index = value_counts.index.astype(object)

        # if we want nans, count the mask
        if not dropna:

            # TODO(extension)
            # appending to an Index *always* infers
            # w/o passing the dtype
            array = np.append(array, [self._mask.sum()])
            index = Index(
                np.concatenate(
                    [index.values, np.array([self.dtype.na_value], dtype=object)]
                ),
                dtype=object,
            )

        return rs.DataSeries(array, index=index)

    
class NumpyFloat32ExtensionDtype(MTZDtype):
    """Base ExtensionDtype class for generic MTZDtype backed by np.float32"""

    type = np.float32
    kind = 'f'
    na_value = np.nan

    @property
    def _is_numeric(self):
        return True

    @cache_readonly
    def numpy_dtype(self):
        """ Return an instance of our numpy dtype """
        return np.dtype(self.type)

    @cache_readonly
    def itemsize(self):
        """ Return the number of bytes in this dtype """
        return self.numpy_dtype.itemsize

class NumpyExtensionArray(ExtensionArray, ExtensionScalarOpsMixin):
    """
    Base ExtensionArray for defining a custom Pandas.ExtensionDtype that
    uses a numpy array on the backend for storing the array data.
    """
    _itemsize = 8
    ndim = 1
    can_hold_na = True
    __array_priority__ = 1000

    def __init__(self, values, copy=False, dtype=None):
        self.data = np.array(values, dtype=self._dtype.type, copy=copy)
    
    @property
    def dtype(self):
        return self._dtype

    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        return cls(scalars, copy=copy, dtype=dtype)

    @classmethod
    def _from_sequence_of_strings(cls, strings, dtype=None, copy=False):
        scalars = to_numeric(strings, errors="raise")
        return cls._from_sequence(scalars, dtype, copy)
    
    @classmethod
    def _from_factorized(cls, values, original):
        return cls(values)

    @classmethod
    def _from_ndarray(cls, data, copy=False):
        return cls(data, copy=copy)

    @property
    def shape(self):
        return self.data.shape

    @property
    def na_value(self):
        return self.dtype.na_value
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        item = check_array_indexer(self, item)

        result = self.data[item]
        if not lib.is_scalar(item):
            result = type(self)(result)
        return result

    @property
    def nbytes(self):
        return self._itemsize * len(self)

    def reshape(self, *args, **kwargs):
        return self.data.reshape(*args, **kwargs)
    
    def _formatter(self, boxed=False):
        def fmt(x):
            if np.isnan(x):
                return "NaN"
            return str(x)
        return fmt

    def copy(self, deep=False):
        return type(self)(self.data.copy())

    def __setitem__(self, key, value):
        value = extract_array(value, extract_numpy=True)

        key = check_array_indexer(self, key)
        scalar_value = lib.is_scalar(value)

        if not scalar_value:
            value = np.asarray(value, dtype=self.data.dtype)

        self.data[key] = value

    def isna(self):
        return np.isnan(self.data)

    def take(self, indexer, allow_fill=False, fill_value=None):
        took = take(self.data, indexer, allow_fill=allow_fill,
                    fill_value=fill_value)
        return type(self)(took)

    @staticmethod
    def _box_scalar(scalar):
        return scalar

    def astype(self, dtype, copy=True):
        """
        Cast to a NumPy array with 'dtype'. Handles special case with 
        MTZDtypes.

        Parameters
        ----------
        dtype : str or dtype
            Typecode or data-type to which the array is cast.
        copy : bool, default True
            Whether to copy the data, even if not necessary. If False,
            a copy is made only if the old dtype does not match the
            new dtype.

        Returns
        -------
        array : ndarray
            NumPy ndarray with 'dtype' for its dtype.
        """
        # Cannot defer to ExtensionArray.astype() due to call to coercion
        # to dtype("float32")
        if isinstance(dtype, MTZDtype):
            if is_dtype_equal(dtype, self.dtype):
                if not copy:
                    return self
                else:
                    return self.copy()
            else:
                return dtype.construct_array_type()._from_sequence(self, copy=False)
        return super().astype(dtype, copy=copy)
        
    @classmethod
    def _concat_same_type(cls, to_concat):
        return cls(np.concatenate([array.data for array in to_concat]))

    def tolist(self):
        return self.data.tolist()

    def unique(self):
        _, indices = np.unique(self.data, return_index=True)
        data = self.data.take(np.sort(indices))
        return self._from_ndarray(data)

    def __iter__(self):
        return iter(self.data)

    def _reduce(self, name, skipna=True, **kwargs):
        data = self.data

        op = getattr(nanops, 'nan' + name)
        result = op(data, axis=0, skipna=skipna)

        return result

    def value_counts(self, dropna=True):
        """
        Returns a DataSeries containing counts of each category.
        Every category will have an entry, even those with a count of 0.

        Parameters
        ----------
        dropna : bool, default True
            Don't include counts of NaN.

        Returns
        -------
        counts : DataSeries
        """
        from pandas import Index
        import reciprocalspaceship as rs

        # compute counts on the data with no nans
        mask = np.isnan(self.data)
        data = self.data[~mask]
        value_counts = Index(data).value_counts()
        array = value_counts.values

        # TODO(extension)
        # if we have allow Index to hold an ExtensionArray
        # this is easier
        index = value_counts.index.astype(object)

        # if we want nans, count the mask
        if not dropna:

            # TODO(extension)
            # appending to an Index *always* infers
            # w/o passing the dtype
            array = np.append(array, [mask.sum()])
            index = Index(
                np.concatenate(
                    [index.values, np.array([self.dtype.na_value], dtype=object)]
                ),
                dtype=object,
            )

        return rs.DataSeries(array, index=index)

    def _coerce_to_ndarray(self, dtype=None):
        if dtype:
            data = self.data.astype(dtype)
        else:
            data = self.data.astype(self.dtype.type)
        return data

    def __array__(self, dtype=None):
        return self._coerce_to_ndarray(dtype=dtype)

NumpyExtensionArray._add_arithmetic_ops()
NumpyExtensionArray._add_comparison_ops()
