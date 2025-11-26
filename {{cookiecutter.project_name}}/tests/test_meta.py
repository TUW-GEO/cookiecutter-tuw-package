from {{ cookiecutter.project_slug }} import greet


def test_that_testing_package_is_working():
    assert True


def test_greet_returns_correctly():
    got = greet()
    want = "Hello from {{ cookiecutter.project_slug }}"

    assert got == want
