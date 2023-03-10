from databases.models import PaymentsLog,Client,Quota,RechargeRate,ClientAdmin

def recharge_quotas_log_payment(amt,user,data):
    context = {}
    amt = amt/100 # converting amount from  paise to rupee
    rate_list = RechargeRate.objects.order_by("-timestamp")[0]
    context['mail_rate'] = int(rate_list.mail_rate)
    context['request_rate'] =int(rate_list.request_rate)
    user = str(user)
    client = ClientAdmin.objects.get(username= user).client
    quota = Quota.objects.get(client = client)
    quota.quantity = int(quota.quantity) + (amt * context['request_rate'])
    quota.mail = int(quota.mail) + (amt * context['mail_rate'])
    quota.save()
    payment_log = PaymentsLog()
    payment_log.client = client
    payment_log.order_id = data['razorpay_order_id']
    payment_log.payment_id = data['razorpay_payment_id']
    payment_log.amount = amt
    payment_log.rate = rate_list
    payment_log.save()