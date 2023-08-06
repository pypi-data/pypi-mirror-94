import os

UNKNOWN_NAME = "unknown"
UNKNOWN_VERSION = "0.0.0"


def get_mvi_manager_url() -> str:
    """Returns a URL where the manager currently running
    this service can be reached.

    Returns:
        str: URL to manager
    """
    return os.environ.get("MVI_MANAGER_URL", "http://host.docker.internal")


def get_mvi_manager_hostname() -> str:
    """Returns the hostname of the manager currently running
    this service.

    Returns:
        str: Hostname of manager
    """
    return os.environ.get("MVI_MANAGER_HOSTNAME", "localhost")


def get_service_name() -> str:
    """Name of this service

    Returns:
        str: Name
    """
    return os.environ.get("mvi.name", UNKNOWN_NAME)


def get_service_version() -> str:
    """Versio of this service

    Returns:
        str: Version string (ex. 1.2.3)
    """
    return os.environ.get("mvi.version", UNKNOWN_VERSION)


def get_service_access_token() -> str:
    """Returns a valid access token for communicating with
    the manager currently running this service and other services
    running on that manager.

    Returns:
        str: JWT token
    """
    return os.environ.get("mvi.auth", "unknown")


def get_service_root_path() -> str:
    """Returns the root path at which this service is running.
    Can be for example `/services/<service_name>_<service_version>`

    Returns:
        str: Root path
    """
    name = get_service_name()
    version = get_service_version()

    if name == UNKNOWN_NAME and version == UNKNOWN_VERSION:
        return ""

    return f"/services/{name}_{version}/"


def get_headers() -> dict:
    """Generating headers for API calls

    Returns:
        dict: Assembled header
    """
    return {
        "Authorization": f"Bearer {get_service_access_token()}",
        "Content-Type": "application/json",
        "Host": get_mvi_manager_hostname(),
    }


def get_authorized_domains() -> list:
    """Returns list of autorized domains for auth header

    Returns:
        list: List of authorized domains
    """
    return [get_mvi_manager_hostname()]
