from bit.core.task import Task

class CXXLink(Task):
    linker = None # No 'linker' is set.

    def __init__(self, *args):
        super().__init__(*args)
        self.attributes.update(dict(
            library[],
            flags=[],
            type=[] # We will 'pop' whatever the type is from the list, so no
                    # worries :v
        ))
