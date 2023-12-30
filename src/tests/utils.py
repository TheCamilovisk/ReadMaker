import inspect
import os
import re

_tests_folder = os.path.split(__file__)[0]


def _process_test_file_name(file_path: str) -> str:
    basename = os.path.basename(file_path)
    raw_name = os.path.splitext(basename)[0]
    name = raw_name.removeprefix("test_")
    return name


def _camel_to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _process_class_name(class_name: str) -> str:
    raw_snake_class_name = _camel_to_snake(class_name)
    snake_class_name = raw_snake_class_name.removeprefix("test_")
    return snake_class_name


def get_resource_path(resource_name: str) -> str:
    caller_frame = inspect.stack()[1]
    frame = caller_frame[0]
    info = caller_frame[1:4]

    file_name = _process_test_file_name(info[0])
    function_name = info[2].removeprefix("test_")

    class_name = None
    if "self" in frame.f_locals:
        raw_class_name = frame.f_locals["self"].__class__.__name__
        class_name = _process_class_name(raw_class_name)

    resource_file_path = os.path.join(
        _tests_folder, "resources", file_name, class_name, function_name, resource_name
    )
    if not os.path.exists(resource_file_path):
        raise ValueError(f"Resource not found: {resource_file_path}")

    return resource_file_path


def get_text_resource(resource_path: str) -> str:
    resource = None
    with open(resource_path, "r") as f:
        resource = f.read()
    return resource
