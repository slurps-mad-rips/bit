from bit.core.context import Context
from bit.core.task import MetaTask

# Targets can only spawn Tasks, but can depend on each other. In these
# instances, a Target will run all of its target dependencies before
# any of its tasks. When the dependencies are being setup, circular
# dependencies are reported, and 'incorrect' dependency nodes are removed.
# (e.g., Target A is a dependency of Target B. Therefore, Target A is removed
#  from Target B's parent's dependency list)

class Target(Context):

    def __init__(self, name, parent): super().__init__(name, parent)

    # Operator overload for a dependency arrow.
    # Allows for something like
    # target << other_target
    # Where the result is that other_target is now run before
    # target. Takes one (and only one) input. Multiple
    # calls must be used when performing the
    # manual dependency setting.
    # i.e.,
    # target << target1
    # target << target2
    def __lshift__(self, other):
        # TODO: Perform circular dependency tracking
        if not isinstance(other, Target):
            raise TypeError('Given dependency is not a Target')
        self.dependencies[other.name] = other
        self.order.append(other.name)
        # Remove other from the workspace
        del self.parent.dependencies[other.name]
        self.parent.order.remove(other.name)
        return self

    def spawn(self, name): return MetaTask.get(name)(name, self)
