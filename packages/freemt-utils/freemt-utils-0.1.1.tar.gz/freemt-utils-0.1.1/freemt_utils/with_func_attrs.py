r"""func attr type check

example use:

@with_func_attrs(a=-1)
def func() -> None:
    '''func'''
    func.a += 1  # pylint: disable=no-member

https://stackoverflow.com/questions/47056059/best-way-to-add-attributes-to-a-python-function
"""
# @with_func_attrs(latex = r'$ax^2 + bx + c$', foo = 'bar')

# from typing import Callable, Union
from typing import Callable, Any


# def with_func_attrs(**attrs: Union[int, str, ]) -> Callable:
def with_func_attrs(**attrs: Any) -> Callable:
    ''' with_func_attrs '''
    def with_attrs(fct: Callable) -> Callable:
        for key, val in attrs.items():
            setattr(fct, key, val)
        return fct
    return with_attrs
