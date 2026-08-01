import pytest
import json
from vector import Vector

def test_constructor_and_iter():
    vec = Vector([1,2,3])
    assert list(vec) == [1.0, 2.0, 3.0]

def test_equal():
    assert Vector([1,2,3]) == Vector([1.0,2.0,3.0])
    assert Vector([1,2,3]) != Vector([1.0,2.0])
    assert Vector([2,1]) != Vector([1.0,2.0])

def test_len():
    v1 = Vector([1,2,3,4,5,6,7,8])
    assert 8 == len(v1)
    assert 0 == len(Vector([]))

def test_slicing_and_get_item():
    v1 = Vector([1,2,3,4,5,6,7,8])
    assert  3 == v1[2]
    assert Vector([3,4,5,6]) == v1[2:6]

def test_immutability():
    v = Vector([1,2,3])
    with pytest.raises(TypeError):
        v[3] = 5

def test_add():
    v1 = Vector([1,2,3])
    v2 = Vector([2,3,4])
    assert Vector([3,5,7]) == (v1 + v2)

def test_wrong_dim_add():
    v1 = Vector([1,2,3])
    v2 = Vector([2,3,4,5])
    with pytest.raises(ValueError):
        v1 + v2    

def test_sub():
    v1 = Vector([1,2,3])
    v2 = Vector([2,3,4])
    assert Vector([1,1,1]) == (v2 - v1)

def test_scalar_multiplication():
    v1 = Vector([1,2,3])
    assert Vector([3,6,9]) == (3 * v1)
    assert Vector([2,4,6]) == (v1 * 2)

def test_dot_product():
    v1 = Vector([1,2,3])
    v2 = Vector([2,3,4])
    assert 20.0 == v1 @ v2
    assert v1 @ v2 == v2 @ v1

def test_json():
    v = Vector([1, 2, 3])
    s = v.to_json()
    data = json.loads(s)
    assert data == [1.0, 2.0, 3.0]

def test_hash():
    v1 = Vector([1, 2, 3])
    v2 = Vector([1.0, 2.0, 3.0])
    assert hash(v1) == hash(v2)
    s = {v1}
    assert v2 in s

def test_repr():
    v = Vector([1, 2, 3])
    r = repr(v)
    assert 'Vector(1.0, 2.0, 3.0)' == r