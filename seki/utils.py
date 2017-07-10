"""
Useful functions
"""

def singleton(cls):
    """turn a class into a singleton class"""
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance