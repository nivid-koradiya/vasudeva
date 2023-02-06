import environ
import razorpay
from vasudeva.vasudeva.settings import BASE_DIR
import os 
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR,'.env')) 
# print(env('RAZOR_KEY_ID'))
client = razorpay.Client(auth=(env('RAZOR_KEY_ID'),env('RAZOR_KEY_SECRET')))
currency = 'INR'
amount = 20000  # Rs. 200
# Create a Razorpay Order
razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
# order id of newly created order.

razorpay_order_id = razorpay_order['id']
callback_url = 'paymenthandler/'

# we need to pass these details to frontend.
context = {}
context['razorpay_order_id'] = razorpay_order_id
# context['razorpay_merchant_key'] = env('RAZOR_KEY_ID')
context['razorpay_amount'] = amount
context['currency'] = currency
context['callback_url'] = callback_url
print(context)