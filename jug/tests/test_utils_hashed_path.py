from os import path

import jug.utils
import jug.task
from jug import value
from jug.backends.dict_store import dict_store
from jug.hash import hash_one


def test_hashed_path_same_content_same_hash(tmpdir):
    """Re-writing the same content does not change the hash (unlike timed_path)."""
    jug.task.Task.store = dict_store()
    test_file = path.join(str(tmpdir), 'test_file')
    with open(test_file, 'wt') as f:
        f.write("Hello World")
    t0 = jug.utils.hashed_path(test_file)
    h0 = hash_one(t0)
    # Overwrite with identical content
    with open(test_file, 'wt') as f:
        f.write("Hello World")
    t1 = jug.utils.hashed_path(test_file)
    h1 = hash_one(t1)
    assert h0 == h1


def test_hashed_path_different_content_different_hash(tmpdir):
    """Changing the file content changes the hash."""
    jug.task.Task.store = dict_store()
    test_file = path.join(str(tmpdir), 'test_file')
    with open(test_file, 'wt') as f:
        f.write("Hello World")
    t0 = jug.utils.hashed_path(test_file)
    h0 = hash_one(t0)
    with open(test_file, 'wt') as f:
        f.write("Goodbye World")
    t1 = jug.utils.hashed_path(test_file)
    h1 = hash_one(t1)
    assert h0 != h1


def test_hashed_path_value_is_path(tmpdir):
    """value() still returns the original path string."""
    jug.task.Task.store = dict_store()
    test_file = path.join(str(tmpdir), 'test_file')
    with open(test_file, 'wt') as f:
        f.write("Hello")
    hp = jug.utils.hashed_path(test_file)
    assert value(hp) == test_file


def test_hashed_path_differs_from_timed_path(tmpdir):
    """hashed_path and timed_path on the same file produce different hashes."""
    jug.task.Task.store = dict_store()
    test_file = path.join(str(tmpdir), 'test_file')
    with open(test_file, 'wt') as f:
        f.write("Hello World")
    h_hashed = hash_one(jug.utils.hashed_path(test_file))
    h_timed = hash_one(jug.utils.timed_path(test_file))
    assert h_hashed != h_timed


def test_hashed_path_include_path_true_different_paths(tmpdir):
    """With include_path=True (default), same content but different paths → different hashes."""
    jug.task.Task.store = dict_store()
    file_a = path.join(str(tmpdir), 'file_a')
    file_b = path.join(str(tmpdir), 'file_b')
    content = "Same content"
    for fp in (file_a, file_b):
        with open(fp, 'wt') as f:
            f.write(content)
    h_a = hash_one(jug.utils.hashed_path(file_a, include_path=True))
    h_b = hash_one(jug.utils.hashed_path(file_b, include_path=True))
    assert h_a != h_b


def test_hashed_path_include_path_false_same_content(tmpdir):
    """With include_path=False, same content in different paths → same hash."""
    jug.task.Task.store = dict_store()
    file_a = path.join(str(tmpdir), 'file_a')
    file_b = path.join(str(tmpdir), 'file_b')
    content = "Same content"
    for fp in (file_a, file_b):
        with open(fp, 'wt') as f:
            f.write(content)
    h_a = hash_one(jug.utils.hashed_path(file_a, include_path=False))
    h_b = hash_one(jug.utils.hashed_path(file_b, include_path=False))
    assert h_a == h_b
