import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--auth",
        action="store",
        default="",
        help="username:token to pass to test functions",
    )


@pytest.fixture(scope="class")
def auth(request):
    request.cls.auth = request.config.getoption("--auth")
    return request.config.getoption("--auth")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "auth: mark test as requiring authentication token"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--auth"):
        # --auth given in cli: do not skip auth-required tests
        return
    skip_auth = pytest.mark.skip(reason="need --auth option to run")
    for item in items:
        if "auth" in item.keywords:
            item.add_marker(skip_auth)
