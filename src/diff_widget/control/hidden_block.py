

class ControlHiddenBlock:  # todo: move to modules
    """Control hidden block to diff widget

    Attributes
    ---
    position : list[int]
        index position hide lines block
    """
    def __init__(self):
        self.block_id = {}
        self.position: list[int] = []

    def save(self, position: int):
        """Save hide lines block
        :param position: Current position hide lines block"""
        self.position.append(position)
