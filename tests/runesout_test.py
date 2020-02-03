import random, string, pytest
from runesout import Board, Rune

floats = [x / 10.0 for x in range(0, 1000, 1)]
chars = [y for y in string.ascii_uppercase]     # all string characters
floats_chars = []   # empty list to store combined strings and floats
for item in floats:
    floats_chars.append(item)   # append all floats
for item in chars:
    floats_chars.append(item)   # append all chars


def array_gen(n, mode: int):
    """Create nxn arrays for testing."""
    if mode == 0:
        _array = [[False for b in range(n)] for b in range(n)]       # nxn matrix of 0s
    elif mode == 1:
        _array = [[True for b in range(n)] for b in range(n)]        # nxn matrix of 1s
    elif mode == 2:
        _array = [[bool(random.randint(0, 1)) for b in range(n)] for b in range(n)]     # nxn matrix of random binary digits
    elif mode == 3:
        _array = [[random.choice(chars) for b in range(n)] for b in range(n)]     # nxn matrix of random characters

    return _array


class TestGrids(object):
    """Test nxn board generation."""
    def test_nxn_grid(self):
        for n in range(2, 10):
            assert Board((n, n)).size == (n, n)

    def test_random_grid(self):
        for n in range(2, 10):
            _random_tuple = (random.randint(2, 100), random.randint(2, 100))
            assert Board(_random_tuple).size == _random_tuple

    @pytest.mark.xfail
    def test_non_int_grid(self):
        for n in range(2, 10):
            _non_int_tuple = (random.choice(floats_chars), random.choice(floats_chars))
            Board(_non_int_tuple)


class TestStartValues(object):
    """Test various start values."""
    def test_all_false_startvalue(self):
        for n in range(2, 10):
            _false = array_gen(n, 0)
            assert Board((n, n), _false).rune_states == _false

    def test_all_true_startvalue(self):
        for n in range(2, 10):
            _true = array_gen(n, 1)
            assert Board((n, n), _true).rune_states == _true

    def test_all_random_binary_startvalue(self):
        for n in range(2, 10):
            _rand_bin = array_gen(n, 2)
            assert Board((n, n), _rand_bin).rune_states == _rand_bin

    @pytest.mark.xfail
    def test_all_random_string_startvalue(self):
        for n in range(2, 10):
            _rand_choice = array_gen(n, 3)
            Board((n, n), _rand_choice)


def rune_swap_test():
    """Test activation of runes."""
    # TODO: add basic test
    # TODO: add random test
    pass

