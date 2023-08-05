import os
import requests
import shutil
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tempfile import gettempdir
from math import pow
import re
from typing_extensions import Literal

retry_strategy = Retry(
    total=4,
    backoff_factor=1,
    status_forcelist=[404, 429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "PUT", "POST", "DELETE", "OPTIONS", "TRACE"],
)
retry_adapter = HTTPAdapter(max_retries=retry_strategy)
requests_retry = requests.Session()
requests_retry.mount("https://", retry_adapter)
requests_retry.mount("http://", retry_adapter)


def create_temp_directory() -> str:
    current_temp_directory = gettempdir()
    temp_path = os.path.join(current_temp_directory, "aquarium_learning_disk_cache")
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    os.makedirs(temp_path)
    return temp_path


def _is_one_gb_available() -> bool:
    """Returns true if there is more than 1 GB available on the current filesystem"""
    return shutil.disk_usage("/").free > pow(1024, 3)  # 1 GB


def assert_valid_name(name: str) -> None:
    is_valid = re.match(r"^[A-Za-z0-9_]+$", name)
    if not is_valid:
        raise Exception(
            "Name {} must only contain alphanumeric and underscore characters".format(
                name
            )
        )


def raise_resp_exception_error(resp):
    if not resp.ok:
        message = None
        try:
            r_body = resp.json()
            message = r_body.get("message") or r_body.get("msg")
        except:
            # If we failed for whatever reason (parsing body, etc.)
            # Just return the code
            raise Exception(
                "HTTP Error received: {}".format(str(resp.status_code))
            ) from None

        if message:
            raise Exception("Error: {}".format(message))
        else:
            raise Exception(
                "HTTP Error received: {}".format(str(resp.status_code))
            ) from None


def determine_latest_version():
    from bs4 import BeautifulSoup
    from http import HTTPStatus
    import requests
    import re

    PACKAGE_REPO_URL = "https://aquarium-not-pypi.web.app/{}".format(__package__)
    SEM_VER_MATCHER = re.compile(f"{__package__}-(.*)\.tar\.gz")

    r = requests.get(PACKAGE_REPO_URL)
    if r.status_code == HTTPStatus.OK:
        # Python package repos have a standard layout:
        # https://packaging.python.org/guides/hosting-your-own-index/
        versions = BeautifulSoup(r.text, "html.parser").find_all("a")
        if len(versions) > 0:
            version_match = SEM_VER_MATCHER.match(versions[-1]["href"])
            if version_match != None:
                return version_match.group(1)
    return None


def check_if_update_needed():
    from importlib_metadata import version
    from termcolor import colored

    current_version = version(__package__)
    latest_version = determine_latest_version()

    if latest_version != None and current_version != latest_version:
        print(
            colored(
                f"aquariumlearning: Please upgrade from version {current_version} to latest version {latest_version}.",
                "yellow",
            )
        )


TEMP_FILE_PATH = create_temp_directory()

TYPE_PRIMITIVE_TO_STRING_MAP = {
    str: "str",
    int: "int",
    float: "float",
    bool: "bool",
}

USER_METADATA_TYPES = Literal["str", "int", "float", "bool"]
POLYGON_VERTICES_KEYS = Literal["vertices"]
POSITION_KEYS = Literal["x", "y", "z"]
ORIENTATION_KEYS = Literal["w", "x", "y", "z"]
KEYPOINT_KEYS = Literal["x", "y", "name"]

MAX_FRAMES_PER_BATCH = 1000
MAX_CHUNK_SIZE = int(pow(2, 23))  # 8 MiB
