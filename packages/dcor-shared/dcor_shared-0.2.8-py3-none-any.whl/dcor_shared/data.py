import pathlib
import time

try:
    from ckan.common import config
except ImportError:
    config = {}


#: Content of the dummy file created when importing data.
DUMMY_BYTES = b"[Data import pending]"


def wait_for_resource(path):
    """Wait for resource if it is uploaded manually

    This function can be used by other plugins to ensure that
    a resource is available for processing.

    The ckanext-dcor_depot plugin imports data by uploading
    dummy files and then hard-linking to data on disk. Here
    we just check that the file is not a dummy file anymore.
    """
    path = pathlib.Path(path)
    dcor_depot_available = "dcor_depot" in config.get('ckan.plugins', "")
    timeout = 10
    t0 = time.time()
    ld = len(DUMMY_BYTES)
    while True:
        if time.time() - t0 > timeout:
            raise OSError("Data import seems to take too long "
                          "for '{}'!".format(path))
        elif not path.exists():
            time.sleep(0.05)
            continue
        elif dcor_depot_available and not path.is_symlink():
            # Resource is only available when it is symlinked by
            # the ckanext.dcor_depot `symlink_user_dataset` job
            # (or by the ckanext.dcor_depot importers).
            time.sleep(0.05)
            continue
        elif path.stat().st_size < 2 * ld:
            with path.open("rb") as fd:
                data = fd.read(ld)
            if data == DUMMY_BYTES:
                # wait a bit
                time.sleep(0.01)
                continue
        else:
            # not a dummy file
            break
