import environ
import razorpay
from vasudeva.settings import BASE_DIR
import os 
def gen_order(amount_rupees):
    env = environ.Env()
    environ.Env.read_env(os.path.join(BASE_DIR,'.env')) 
    # print(env('RAZOR_KEY_ID'))
    client = razorpay.Client(auth=(env('RAZOR_KEY_ID'),env('RAZOR_KEY_SECRET')))
    currency = 'INR'
    amount = amount_rupees 
    amount = amount * 100 # converting inr to paise
    # Create a Razorpay Order
    razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    # order id of newly created order.

    razorpay_order_id = razorpay_order['id']
    callback_url = 'handler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    # context['razorpay_merchant_key'] = env('RAZOR_KEY_ID')
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['razorpay_merchant_key'] = env('RAZOR_KEY_ID')
    return context