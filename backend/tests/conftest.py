import pytest
@pytest.fixture(scope='session')
def artifacts(tmp_path_factory):
    from src.training_pipeline import run
    root = tmp_path_factory.mktemp('iris-artifacts')
    run(root, with_eda=False)
    return root
