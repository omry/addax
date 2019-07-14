from antelope import Antelope


def test_basic():
    s = "{99, 3, 451}"
    antelope = Antelope(s)
    print(antelope)

# def get_test_files():
#     return [
#         ('a', 1),
#         ('b', 2),
#         ('c', 3),
#         ('d', 4),
#     ]
#
#
# @pytest.mark.parametrize('test_name,file', get_test_files())
# def test_foo(test_name, file):
#   pass
