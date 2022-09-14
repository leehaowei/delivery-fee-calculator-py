from fastapi import FastAPI
from src.app.FeeCalculator import FeeCalculator
from src.app.Order import Order
import src.app.Constants as C

app = FastAPI()


@app.get("/")
async def read_main():
    return {"welcome msg": "Welcome to Foodmorsa"}


@app.post("/fee/")
def get_delivery_fee(order: Order):
    base_delivery_fee = C.BASE_DELIVERY_FEE
    calculator = FeeCalculator(order)
    surcharge_cart_value = calculator.cart_value_surcharge()
    extra_delivery_amount = calculator.extra_delivery_fee()
    surcharge_items = calculator.items_surcharge()
    delivery_fee = base_delivery_fee + surcharge_cart_value + extra_delivery_amount + surcharge_items

    if calculator.is_friday_rush():   # check whether the delivery time is in Friday rush (3 - 7 PM UTC)
        delivery_fee *= 1.1

    delivery_fee = calculator.check_max_delivery_fee(delivery_fee)

    delivery_fee = int(delivery_fee)  # make sure delivery_fee is integer
    return {"delivery_fee": delivery_fee}
