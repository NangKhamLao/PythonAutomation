import pytest

@pytest.mark.smoke
def test_group1():
    assert True

@pytest.mark.regression
def test_group2():
    assert True

@pytest.mark.smoke
def test_group3():
    assert True

@pytest.mark.skip(reason="Test is not completed yet.")
def test_skip():
    print("*********")
    assert False

