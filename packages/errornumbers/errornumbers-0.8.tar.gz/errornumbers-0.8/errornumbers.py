import math


class ErrorNumber:
    """
    A ErrorNumber object represents a *real* number with some real error

    Attributes *value*, *absolute_error*, and *relative error* are all floats.
    """

    def __init__(self, value, error, relative=False):
        """
        Creates a ErrorNumber object

        :param value: (int or float)
        :param error: (int or float)
        :param relative: Whether to interpret the error given in the parameter above as a relative or absolute error.
            (bool) (default value: False -> (absolute error))
        """
        assert error > 0, "Error must be positive!"
        if relative:
            self.value = float(value)
            self.relative_error = float(error)
            self.absolute_error = self.relative_error * self.value
        else:
            self.value = float(value)
            self.absolute_error = float(error)
            self.relative_error = float(error) / float(value)

    #overloaders for standard python methods can be found below these methods

    def plus(self, other):
        """
        Adds two ErrorNumber objects.
        Error is calculated by adding absolute error values.
        Please use "+" instead of this function wherever possible.

        :param other: (ErrorNumber)
        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return ErrorNumber(self.value + other.value, self.absolute_error + other.absolute_error)

    def plusc(self, constant):
        """
        Adds a constant to an Errornumber
        Error doesn't change.
        Please use "+" instead of this function wherever possible.


        :param constant: (int or float)
        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return ErrorNumber(self.value + constant, self.absolute_error)

    def minus(self, other):
        """
        Subtracts a ErrorNumber obect from another.
        Error is calculated by adding absolute error values.
        Please use "-" instead of this function wherever possible.

        :param other: (ErrorNumber)
        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return ErrorNumber(self.value - other.value, self.absolute_error + other.absolute_error)

    def minusc(self, constant):
        """
        Subtracts a constant from a ErrorNumber object.
        Error doesn't change.
        Please use "-" instead of this function wherever possible.

        :param constant: (int or float)
        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return ErrorNumber(self.value - constant, self.absolute_error)

    def times(self, other):
        """
        Multiplies ErrorNumber objects.
        Error is calculated by adding relative errors.
        Please use "*" instead of this function wherever possible.

        :param other: (ErrorNumber)
        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return ErrorNumber(self.value * other.value, self.relative_error + other.relative_error, relative=True)

    def timesc(self, constant):
        """
        Multiplies a ErrorNumber by a constant.
        Error doesn't change.
        Please use "*" instead of this function wherever possible.

        :param constant: (float or int)
        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return ErrorNumber(self.value * constant, self.relative_error, relative=True)

    def divided_by(self, other):
        """
        Divides a ErrorNumber by another ErrorNumber.
        Error is calculated by adding relative errors.
        Please use "/" instead of this function wherever possible.
        (Dividing by 0 doesn't work, even if the error range implies otherwise).

        :param other: (ErrorNumber)
        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return ErrorNumber(self.value / other.value, self.relative_error + other.relative_error, relative=True)

    def divided_byc(self, constant):
        """
        Divides a ErrorNumber by a constant.
        Error doesn't change.
        Please use "/" instead of this function wherever possible.
        (Dividing by 0 doesn't work, even if the error range implies otherwise).

        :param constant: (float or int)
        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return ErrorNumber(self.value / constant, self.relative_error, relative=True)

    def inverse(self):
        """
        Returns the inverse of a ErrorNumber object.
        Relative Error doesn't change.
        "1 / x" works as well.

        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return ErrorNumber((1 / self.value), self.relative_error, relative=True)

    def squared(self):
        """
        Returns the square of a ErrorNumber object.
        Relative Error doubles.

        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return self.times(self)

    def cubed(self):
        """
        Returns the cube of a ErrorNumber object.
        Relative Error triples.

        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return self.times(self).times(self)

    def to_the(self, constant):
        """
        Exponentiates a ErrorNumber object to a certain constant.
        Relative Error is given by | original_relative_error * constant |

        :param constant: (float or int)
        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return ErrorNumber(self.value ** constant, math.fabs(self.relative_error * constant), relative=True)

    def sqrt(self):
        """
        Take the square root of a ErrorNumber.
        Relative Error halves.
        As ErrorNumbers represent real numbers, avoid taking square roots of negative numbers!

        :return: (ErrorNumber) **Doesn't change original objects**
        """
        return self.to_the(1 / 2)

    def __add__(self, other):
        if isinstance(other, ErrorNumber):
            return self.plus(other)
        elif isinstance(other, (float, int)):
            return self.plusc(other)
        else:
            raise TypeError("Type must be either ErrorNumber, float or int")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, ErrorNumber):
            return self.minus(other)
        elif isinstance(other, (float, int)):
            return self.minusc(other)
        else:
            raise TypeError("Type must be either ErrorNumber, float or int")

    def __mul__(self, other):
        if isinstance(other, ErrorNumber):
            return self.times(other)
        elif isinstance(other, (float, int)):
            return self.timesc(other)
        else:
            raise TypeError("Type must be either ErrorNumber, float or int")

    def __pow__(self, power, modulo=None):
        assert modulo is None, "Not implemented"
        if isinstance(power, (float, int)):
            return self.to_the(power)
        else:
            raise TypeError("Type must be either float or int")

    def __truediv__(self, other):
        if isinstance(other, ErrorNumber):
            return self.divided_by(other)
        elif isinstance(other, (float, int)):
            return self.divided_byc(other)
        else:
            raise TypeError("Type must be either ErrorNumber, float or int")

    def __rtruediv__(self, other):
        if isinstance(other, ErrorNumber):
            return other.times(self.inverse())
        elif isinstance(other, (float, int)):
            inv = self.inverse()
            return ErrorNumber(other * inv.value, inv.relative_error, relative=True)
        else:
            raise TypeError("Type must be either ErrorNumber, float or int")

    def __str__(self):
        return "[value={}; error={}; relative_error={}]".format(self.value, self.absolute_error, self.relative_error)


def sin(e_n):
    '''
    :param e_n: an ErrorNumber (IN RADIANS)
    :return: the sinus of that ErrorNumber

    :example:
    >>> x = ErrorNumber(1.5708, 0.1)
    >>> sin(x).value
    0.9999999999932537
    >>> sin(x).absolute_error
    3.673205103346574e-07
    '''
    value = math.sin(e_n.value)
    abs_error = abs(math.cos(e_n.value) * e_n.absolute_error)
    return ErrorNumber(value, abs_error)


def cos(e_n):
    '''
    :param e_n: an ErrorNumber (IN RADIANS)
    :return: the cosinus of that ErrorNumber

    :example:
    >>> x = ErrorNumber(1.3, 0.1)
    >>> cos(x).value
    0.26749882862458735
    >>> cos(x).absolute_error
    0.0963558185417193
    '''
    value = math.cos(e_n.value)
    abs_error = abs(math.sin(e_n.value) * e_n.absolute_error)
    return ErrorNumber(value, abs_error)


def tan(e_n):
    '''
    :param e_n: an ErrorNumber (IN RADIANS)
    :return: the tangens of that ErrorNumber

    :example:
    >>> x = ErrorNumber(0.5, 0.1)
    >>> tan(x).value
    0.5463024898437905
    >>> tan(x).absolute_error
    0.11394939273245491
    '''
    value = math.sin(e_n.value) / math.cos(e_n.value)
    abs_error = abs((1 / (math.cos(e_n.value)**2)) * e_n.absolute_error)
    return ErrorNumber(value, abs_error)


def cot(e_n):
    '''
    :param e_n: an ErrorNumber (IN RADIANS)
    :return: the cotangens of that ErrorNumber

    :example:
    >>> x = ErrorNumber(0.5, 0.1)
    >>> cot(x).value
    0.5463024898437905
    >>> cot(x).absolute_error
    0.20858296429334883
    '''
    value = math.cos(e_n.value) / math.sin(e_n.value)
    abs_error = abs((1 / math.sin(e_n.value)**2) * e_n.absolute_error)
    return ErrorNumber(value, abs_error)


def exp(e_n):
    '''
    :param e_n: an ErrorNumber
    :return: e^x of that ErrorNumber

    :example:
    >>> x = ErrorNumber(1, 0.1)
    >>> exp(x).value
    2.718281828459045
    >>> exp(x).absolute_error
    0.27182818284590454
    '''
    value = math.e ** e_n.value
    error = value * e_n.absolute_error
    return ErrorNumber(value, error)


def expbase(e_n, base):
    '''
    :param e_n: an ErrorNumber
    :param base: a base (any real number)
    :return: base^x of that ErrorNumber

    :example:
    >>> x = ErrorNumber(2, 0.1)
    >>> expbase(x, 3).value
    9
    >>> expbase(x, 3).absolute_error
    0.9
    '''
    value = base ** e_n.value
    error = value * e_n.absolute_error
    return ErrorNumber(value, error)


def from_non_reproducible(lort):
    '''
    creates an ErrorNumber from input data, calculating an average and a standard deviation
    The absolute error that is returned is three times the standard deviation calculated

    The stdev is calculated using factor 1/ (n(n-1))

    :param lort: List or tuple containing the datapoints

    :example:
    >>> x = from_non_reproducible([1, 2, 3, 4])
    >>> x.value
    2.5
    >>> x.absolute_error
    1.9364916731037085
    '''
    # compute an average
    average = sum(lort) / len(lort)
    sum_of_of_quad_diffs = sum([(x - average) ** 2 for x in lort])
    fout = math.sqrt((1 / (len(lort) * (len(lort) - 1))) * sum_of_of_quad_diffs)
    return ErrorNumber(average, fout * 3)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
