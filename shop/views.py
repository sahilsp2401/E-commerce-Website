from django.shortcuts import render
from django.http import HttpResponse
from . models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from Paytm import checksum
MERCHANT_KEY = 'kbzk1DSbJiv_O3p5'
# Create your views here.
def index(request):
    allProds = []
    catProds = Product.objects.values('category','id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])
    params = {'allProds':allProds}
    return render(request,'shop/index.html',params)


def searchMatch(query,item):
    #return true if query matches item
    query = query.lower()
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search','')
    allProds = []
    catProds = Product.objects.values('category','id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query,item) ]
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        if len(prod) != 0 :
            allProds.append([prod,range(1,nSlides),nSlides])
    params = {'allProds':allProds,'msg':""}
    if(len(allProds)) == 0 or len(query)<4:
        params = {'msg':"Please make sure to enter relevant search query!!! "}
    return render(request,'shop/search.html',params)


def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name','')
        email = request.POST.get('mail','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
    return render(request,'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        email = request.POST.get('email','')
        order_id = request.POST.get('orderid','')
        try:
            order = Orders.objects.filter(order_id=order_id,email=email)
            if len(order)>0:
                update =  OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':f"{item.timestamp.strftime('%A')}, Date-{item.timestamp}"})
                    response = json.dumps({'status':"success","updates":updates,"itemsJson":order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noItem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request,'shop/tracker.html')


def productView(request,myid): #we are getting this myid from urls.py
    #Fetch the product using ID
    product = Product.objects.filter(id=myid)
    params={'product':product[0]}
    return render(request,'shop/prodView.html',params)

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson','')
        amount = request.POST.get('amount','')
        name = request.POST.get('name','')
        email = request.POST.get('mail','')
        address = request.POST.get('add1','') + " " + request.POST.get('add2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip','')
        phone = request.POST.get('phone','')
        order = Orders(items_json=items_json,amount=amount,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id,update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
    #     # Request paytm to transfer the amount to your account after payment by user
    #     param_dict={
    #         'MID': 'WorldP64425807474247',
    #         'ORDER_ID': str(order.order_id),
    #         'TXN_AMOUNT': str(amount),
    #         'CUST_ID': email,
    #         'INDUSTRY_TYPE_ID': 'Retail',
    #         'WEBSITE': 'WEBSTAGING',
    #         'CHANNEL_ID': 'WEB',
    #         'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/'
    #     }
    #     param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict,MERCHANT_KEY)
    #     return  render(request,'shop/paytm.html',{'param_dict':param_dict})
    return render(request, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
     # paytm will send you post request here
    return HttpResponse('Successful')
    # form = request.POST
    # response_dict = {}
    # for i in form.keys():
    #     response_dict[i] = form[i]
    #     if i == 'CHECKSUMHASH':
    #         check = form[i]

    # verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, check)
    # if verify:
    #     if response_dict['RESPCODE'] == '01':
    #         print('order successful')
    #     else:
    #         print('order was not successful because' + response_dict['RESPMSG'])
    # return render(request, 'shop/paymentstatus.html', {'response': response_dict})