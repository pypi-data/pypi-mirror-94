import sys


class python_path:
    '''
    Context manager to temporary modify sys.path
    '''
    def __init__(self, paths):
        if not isinstance(paths, list):
            paths = [paths]
        self.paths = paths
        self.prev_path = sys.path
        
    def __enter__(self):
        sys.path = self.paths + sys.path
        
    def __exit__(self, *args):
        sys.path = self.prev_path
        
