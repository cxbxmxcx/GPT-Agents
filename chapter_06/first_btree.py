import py_trees


# Define the conditions and actions
class HasApple(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(HasApple, self).__init__(name)

    def update(self):
        # Condition check (placeholder for actual logic)
        if True:  # Replace with actual condition
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


class EatApple(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(EatApple, self).__init__(name)

    def update(self):
        # Action (placeholder for actual action)
        print("Eating apple")
        return py_trees.common.Status.SUCCESS


class HasPear(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(HasPear, self).__init__(name)

    def update(self):
        # Condition check (placeholder for actual logic)
        if True:  # Replace with actual condition
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


class EatPear(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(EatPear, self).__init__(name)

    def update(self):
        # Action (placeholder for actual action)
        print("Eating pear")
        return py_trees.common.Status.SUCCESS


# Create the behavior tree nodes
has_apple = HasApple(name="Has apple")
eat_apple = EatApple(name="Eat apple")
sequence_1 = py_trees.composites.Sequence(name="Sequence 1", memory=True)
sequence_1.add_children([has_apple, eat_apple])

has_pear = HasPear(name="Has pear")
eat_pear = EatPear(name="Eat pear")
sequence_2 = py_trees.composites.Sequence(name="Sequence 2", memory=True)
sequence_2.add_children([has_pear, eat_pear])

root = py_trees.composites.Selector(name="Selector", memory=True)
root.add_children([sequence_1, sequence_2])

# Create the behavior tree
behavior_tree = py_trees.trees.BehaviourTree(root)

# Execute the behavior tree
py_trees.logging.level = py_trees.logging.Level.DEBUG
for i in range(1, 4):
    print("\n------------------ Tick {0} ------------------".format(i))
    behavior_tree.tick()
