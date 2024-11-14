

class ControlHiddenBlock:
    """Control hidden block to diff widget

    Attributes
    ---
    position : list[int]
        index position hide lines block
    """
    def __init__(self):
        self.__current_id_block: int = 0
        self.block_id = {}
        self.position: list[int] = []

    def get_block_id(self, index_position_block: int) -> int:
        """Getting block ID by its position
        :param index_position_block: Block position in widget
        :return: ID block"""
        for key, value in self.block_id.items():
            if value['position'] == index_position_block:
                return key

    def save(self, position: int):
        """Save hide lines block
        :param position: Current position hide lines block"""
        self.position.append(position)

        self.block_id[self.__current_id_block] = {
            "position": position
        }

        self.__current_id_block += 1
