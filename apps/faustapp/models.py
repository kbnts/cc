import faust


class ItemRecord(faust.Record):
    """
    Expected data structure for the Item model
    """

    cart_uuid: str
    external_id: str
    name: str = ""
    value: int = 0
