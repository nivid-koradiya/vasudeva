import razorpay
import environ
from  vasudeva.settings import BASE_DIR
import os
from .payment_mapper import recharge_quotas_log_payment
def verify_payment(request):
    payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_order_id = request.POST.get('razorpay_order_id', '')
    signature = request.POST.get('razorpay_signature', '')
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    env = environ.Env()
    environ.Env.read_env(os.path.join(BASE_DIR,'.env')) 
    # print(env('RAZOR_KEY_ID'))
    client = razorpay.Client(auth=(env('RAZOR_KEY_ID'),env('RAZOR_KEY_SECRET')))

    result = client.utility.verify_payment_signature(params_dict)
    if result is not None:
        try:
            order = client.order.fetch(razorpay_order_id)
            client.payment.capture(payment_id, order['amount'])
            recharge_quotas_log_payment(int(order['amount']),request.user,params_dict)
            return True
        except: 
            return False
    else:
        return False
    