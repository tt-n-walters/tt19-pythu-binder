class FilePath:
    def __init__(self, *locations):
        self.locations = []
        self.add(*locations)

    # Predicate function
    def _check(self, location):
        invalids = "<>\\/?*|\""
        checks = []
        for char in invalids:
            checks.append(char in location)
        return not any(checks)

    def add(self, *locations):
        """ Add new file/folder names to the path
        """
        for loc in locations:
            if self._check(loc):
                self.locations.append(loc)
            else:
                raise NameError

    def remove(self, *locations):
        for loc in locations:
            if loc == self.locations[-1]:
                self.locations.pop()
            else:
                raise AttributeError

    def __len__(self):
        return len(self.locations)

    def __fspath__(self):
        return "/".join(self.locations)

    def __add__(self, other):
        return FilePath(self.locations + other.locations)


def requires_FilePath(fn):
    def wrapper(*args, **kwargs):
        for arg in args:
            if type(arg) is FilePath:
                break
        else:
            raise TypeError("Locations must be FilePaths")

        # Code reached when at least 1 arg in a FilePath
        return fn(*args, **kwargs)
    return wrapper
