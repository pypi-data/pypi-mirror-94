#!/usr/bin/env python

"""
Time Series.
"""

import numpy as np

from pyrqa.exceptions import UnsupportedDataTypeException, \
    InconsistentDimensionalityException

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2021 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"

SUPPORTED_DATA_TYPES = (np.dtype('float16'),
                        np.dtype('float32'),
                        np.dtype('float64'))


class TimeSeries(object):
    """
    Time series.
    The reconstruction of vectors is conducted using the time delay method.

    :ivar dtype: Data type of the time series data.
    :ivar data: Time series data.
    :ivar embedding_dimension: Embedding dimension.
    :ivar time_delay: Time delay.
    """
    def __init__(self,
                 data,
                 dtype=np.float32,
                 embedding_dimension=2,
                 time_delay=2):
        self.dtype = dtype
        self.data = data
        self.embedding_dimension = embedding_dimension
        self.time_delay = time_delay

    @property
    def dtype(self):
        return self.__dtype

    @dtype.setter
    def dtype(self,
              dtype):
        if dtype not in SUPPORTED_DATA_TYPES:
            raise UnsupportedDataTypeException("Data type '%s' is not supported. Please select either numpy data type float16, float32 or float64." % dtype)

        self.__dtype = dtype

    @property
    def data(self):
        return np.array(self.__data,
                        dtype=self.dtype)

    @data.setter
    def data(self,
             data):
        self.__data = np.array(data,
                               dtype=self.dtype)

    @property
    def length(self):
        """
        Length of data.
        """
        return len(self.data)

    @property
    def offset(self):
        """
        Time series offset based on embedding dimension and time delay.
        """
        return (self.embedding_dimension - 1) * self.time_delay

    @property
    def number_of_vectors(self):
        """
        Number of vectors based on the offset.
        """
        if self.length - self.offset < 0:
            return 0

        return self.length - self.offset

    def get_sub_vectors_as_rows(self,
                                start,
                                count):
        """
        Get row-oriented sub vectors from the original time series.

        :param start: Start index within the original time series.
        :param count: Number of data points to be extracted.
        :returns: Extracted rows.
        """
        return np.array(self.get_sub_columns(start,
                                             count),
                        dtype=self.dtype).transpose().ravel()

    def get_vectors_as_rows(self):
        """
        Get row-oriented vectors from the original time series as one-dimensional array.

        :returns: All vectors.
        """
        return self.get_sub_vectors_as_rows(0,
                                            self.number_of_vectors)

    def get_sub_columns(self,
                        start,
                        count):
        """
        Get sub columns from the original time series.

        :param start: Start index within the original time series.
        :param count: Number of data points to be extracted.
        :returns: Extracted columns.
        """
        columns = []

        for dim in np.arange(self.embedding_dimension):
            offset = dim * self.time_delay
            columns.append(self.data[(start + offset):(start + offset + count)])

        return np.array(columns,
                        dtype=self.dtype)

    def get_sub_vectors_as_columns(self,
                                   start,
                                   count):
        """
        Get column-oriented sub vectors from the original time series.

        :param start: Start index within the original time series.
        :param count: Number of data points to be extracted.
        :returns: Extracted columns.
        """
        return np.array(self.get_sub_columns(start,
                                             count),
                        dtype=self.dtype).ravel()

    def get_sub_series(self,
                       start,
                       count):
        """
        Get sub time series from the original time series.

        :param start: Start index within the original time series.
        :param count: Number of data points to be extracted.
        :returns: Extracted sub time series.
        """
        return self.data[start:start + count + self.offset]


class EmbeddedSeries(object):
    """
    Time series that is already embedded in a multidimensional space.

    :ivar dtype: Data type of the time series data.
    :ivar data: Data of the embedded time series.
    """
    def __init__(self,
                 data,
                 dtype=np.float32):
        self.dtype = dtype
        self.data = data

    @property
    def dtype(self):
        return self.__dtype

    @dtype.setter
    def dtype(self,
              dtype):
        if dtype not in SUPPORTED_DATA_TYPES:
            raise UnsupportedDataTypeException("Data type '%s' is not supported. Please select either numpy data type float16, float32 or float64." % dtype)

        self.__dtype = dtype

    @property
    def data(self):
        return np.array(self.__data,
                        dtype=self.dtype)

    @data.setter
    def data(self,
             data):
        self.__data = np.array(data,
                               dtype=self.dtype)

    @property
    def embedding_dimension(self):
        """
        Embedding dimension.
        """
        try:
            return self.data.shape[1]
        except IndexError:
            raise InconsistentDimensionalityException("The dimensionality of the multi-dimensional vectors is inconsistent.")

    @property
    def number_of_vectors(self):
        """
        Number of vectors within the embedded time series.
        """
        return len(self.data)

    def get_sub_vectors_as_rows(self,
                                start,
                                count):
        """
        Get row-oriented sub vectors from the embedded time series as one-dimensional array.

        :param start: Start index within the original time series.
        :param count: Number of vectors to be extracted.
        :returns: Extracted vectors.
        """
        return np.array(self.data[start:start+count],
                        dtype=self.dtype).ravel()

    def get_vectors_as_rows(self):
        """
        Get row-oriented vectors from the embedded time series as one-dimensional array.

        :returns: All vectors.
        """
        return np.array(self.data,
                        dtype=self.dtype).ravel()

    def get_sub_vectors_as_columns(self,
                                   start,
                                   count):
        """
        Get column-oriented sub vectors from the embedded time series as one-dimensional array.

        :param start: Start index within the original time series.
        :param count: Number of vectors to be extracted.
        :returns: Extracted vectors.
        """
        return np.array(self.data[start:start+count],
                        dtype=self.dtype).transpose().ravel()