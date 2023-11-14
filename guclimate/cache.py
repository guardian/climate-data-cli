import os
import uuid

"""Path to cache directory ([project root]/.cache)"""
__cache_path__ = os.path.join(os.path.dirname(__file__), "../.cache")

# create .cache folder if it does not exist
if not os.path.isdir(__cache_path__):
    os.makedirs(__cache_path__)


"""Generate file name based on a UUID"""
def uniqueFilename() -> str:
    filename = uuid.uuid4().hex
    return filename

def cacheDirectory():
    return __cache_path__