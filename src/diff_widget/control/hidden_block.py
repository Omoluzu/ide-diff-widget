

class HiddenBlock:
    """implementation of information of a specific hidden block of code"""
    def __init__(self, position: int, id_block: int) -> None:
        """Initiation
        :param position: Current position hide lines block
        :param id_block: Identifier hidden block"""
        self.position = position
        self.id = id_block

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"position={self.position}, "
            f"id_block={self.id})"
        )


class ControlHiddenBlock:
    """Control hidden block to diff widget

    Attributes
    ---
    position : list[int]
        index position hide lines block
    """
    def __init__(self):
        self.__current_id_block: int = 0
        self.block_id: dict[int, HiddenBlock] = {}
        self.position: list[int] = []

    # def get_block_id(self, index_position_block: int) -> int:  # fixme
    #     """Getting block ID by its position
    #     :param index_position_block: Block position in widget
    #     :return: ID block"""
    #     for key, value in self.block_id.items():
    #         if value.position == index_position_block:
    #             return key

    def get_block(self, index_position_block: int) -> HiddenBlock:
        """Getting block ID by its position
        :param index_position_block: Block position in widget
        :return: HiddenBlock"""
        return self.block_id[index_position_block]

    def save(self, position: int) -> None:
        """Save hide lines block
        :param position: Current position hide lines block"""
        self.position.append(position)

        self.block_id[position] = HiddenBlock(
            position=position, id_block=self.__current_id_block
        )

        self.__current_id_block += 1
