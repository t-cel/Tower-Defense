from pygame import *
import utils
from typing import Union
from typing import Tuple
from typing import List

# todo: make resource loader able to keep info about assets to load to the time we actually want
# todo: to load it.
# todo: 1. add info about assets to load
# todo: 2. start loading all assets, partly, and show progress, blocking current thread on load

ImagesPack = List[Surface]

image_resources = {}
images_pack_resources = {}

def get_resource_id_and_container(resource_path : Union[str, list],
                                  resource_type : Union[Surface, ImagesPack]) -> Tuple[str, dict]:
    target_container = {}
    target_id = resource_path
    if resource_type is Surface:
        target_container = image_resources
    elif resource_type is ImagesPack:
        target_container = images_pack_resources
        target_id = resource_path[0] # id's of images pack are theirs first items
    else:
        raise Exception("Tried to get resource of not supported type from ResourceCache: " + str(resource_type))
    return target_id, target_container

"""
    Tries to add resource of specified type to cache.
    
    :param **kwargs: additional key-value parameters needed to properly load resource
"""
def add_resource(resource_path : Union[str, list],
                 resource_type : Union[Surface, ImagesPack],
                 **kwargs):
    target_id, target_container = get_resource_id_and_container(resource_path, resource_type)
    resource_exists = target_id in target_container.keys()

    # add the same resource with different id
    if kwargs.get("clone") and resource_exists:
        # print("making clone")
        num = 0
        while target_id + str(num) in target_container.keys():
            num += 1
        target_id = target_id + str(num)

    if resource_exists and not kwargs.get("clone"):
        print("WARNING: Tried to add resource that is already in cache. ID: " + target_id)
        return

    """
    if not isinstance(resource_path, str):
        for item in resource_path:
            print("INFO: adding resource: " + item)
    else:
        print("INFO: adding resource: " + resource_path)
    """

    if resource_type is Surface:
        image_resources[resource_path] = utils.load_image(resource_path, kwargs.get("alpha"))
    elif resource_type is ImagesPack:
        images = []
        for path in resource_path:
            images.append(utils.load_image(path, kwargs.get("alpha")))
        images_pack_resources[target_id] = images

"""
    Returns resource if it exists in cache, if not - tries to add resource and then returns it
    
    :param **kwargs: additional key-value parameters needed to properly load resource, if it's not present in cache
"""
def get_resource(resource_path : Union[str, list],
                 resource_type : Union[Surface, ImagesPack],
                 **kwargs):
    target_id, target_container = get_resource_id_and_container(resource_path, resource_type)

    if target_id in target_container.keys() and not kwargs.get("clone"):
        return target_container[target_id]
    else:
        add_resource(resource_path, resource_type, **kwargs)
        return target_container[target_id]
