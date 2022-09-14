from dateutil import parser
from src.app.Order import Order


class FeeCalculator:

    def __init__(self, order: Order):
        self.order = order
        self.cart_value = order.cart_value
        self.delivery_distance = order.delivery_distance
        self.number_of_items = order.number_of_items
        self.time = order.time

    def cart_value_surcharge(self) -> int:
        surcharge_cart_value = 0
        if self.order.cart_value < 1000:
            surcharge_cart_value = 1000 - self.order.cart_value
        return surcharge_cart_value

    def extra_delivery_fee(self) -> int:
        extra_delivery_amount = 0
        if self.order.delivery_distance > 1000:
            extra_distance = self.order.delivery_distance - 1000
            extra_unit = extra_distance // 500 + 1
            extra_delivery_amount = extra_unit * 100
        return extra_delivery_amount

    def items_surcharge(self) -> int:
        surcharge_items = 0
        if self.order.number_of_items > 4:
            extra_items = self.order.number_of_items - 4
            surcharge_items = extra_items * 500
        return surcharge_items

    def check_max_delivery_fee(self, delivery_fee: int) -> int:
        if delivery_fee > 15_000:
            delivery_fee = 15_000

        if self.order.cart_value >= 100_000:
            delivery_fee = 0

        return delivery_fee

    def is_friday_rush(self) -> bool:
        delivery_time = parser.parse(self.order.time)

        # "Friday rush"
        if delivery_time.weekday() == 4:  # 4 as Friday
            if 15 <= delivery_time.hour <= 19:
                return True
        return False
