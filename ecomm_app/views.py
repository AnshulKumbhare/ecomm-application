from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import product, cart, order
from django.db.models import Q
import random
import razorpay

# Create your views here.



def contact(request):
    return HttpResponse("<h2 style = 'text-shadow: 5px 5px 4px black;'>Welcome to contact page</h2>")

def placement(request):
    return HttpResponse("<b style = 'display: block;'>Placement</b>")

def edit(request, rid):
    print("Id to be edited", rid)
    return HttpResponse("id to be edited:" + rid)


def delete(request, rid):
    print("Id to be deleted: ", rid)
    return HttpResponse("Id to be deleted : " + rid)


class SimpleView(View):
    def get(self, request):
        return HttpResponse("Hello from simple view")
    

def hello(request):
    context = {}
    context['greet'] = "good morning"
    context['x'] = 10
    context['y'] = 20
    context['l'] = [1, 2, 3, 4, 5]
    context['product'] = [
        {'id' : 1, 'name' : 'Harry', 'category' : 'phone', 'price' : 20000},
        {'id' : 2, 'name' : 'Mac', 'category' : 'Laptop', 'price' : 100000},
        {'id' : 3, 'name' : 'Shree', 'category' : 'TV', 'price' : 50000}
    ]

    return render(request, 'hello.html', context)


def index(request):
    context = {}
    p = product.objects.filter(is_active = True)
    context['products'] = p
    # print(p)
    return render(request, 'index.html', context)


def pdetails(request, pid):
    p = product.objects.filter(id = pid)
    context = {}
    context['products'] = p
    return render(request, 'product_details.html', context)

def register(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        upass = request.POST['upass']
        ucpass = request.POST['ucpass']
        if uname == "" or upass == "" or ucpass == "":
            context = {}
            context['errmsg'] = "Fields cannot be empty"
            return render(request, 'register.html', context)
        elif upass != ucpass:
            context = {}
            context['errmsg'] = "Password did not match"
            return render(request, 'register.html', context)
        else:
            try:
                u = User.objects.create(username = uname ,password = upass, email = uname)
                u.set_password(upass)
                u.save()
                context = {}
                context['success'] = "User created successfully"
                return render(request, 'register.html', context)
                # return HttpResponse("Data is Fetched Successfully")
            except Exception:
                context = {}
                context['errmsg'] = "Username already exits"
                return render(request, 'register.html', context)
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        upass = request.POST['upass']
        if uname == "" or upass == "":
            context = {}
            context['errmsg'] = "Field cannot be empty"
            return render(request, 'login.html', context)
        else:
            u = authenticate(username = uname, password = upass)
            if u is not None:
                #login
                login(request, u)
                return redirect('/index')
            # print(u)
            else:
                context = {}
                context['errmsg'] = "invalid Username or Password"
                return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')
    


def user_logout(request):
    logout(request)
    return redirect("/index")


def catfilter(request, cv):
    q1 = Q(is_active = True)      
    q2 = Q(category = cv)
    p = product.objects.filter(q1 & q2)
    context = {}
    context['products'] = p
    return render(request, 'index.html', context)


def sort(request, sv):
    if sv == '0':
        col = 'price'  #Ascending Order
    else:
        col = '-price' # Decending Order
    
    p = product.objects.order_by(col)
    context = {}
    context['products'] = p
    return render(request, 'index.html', context)

def range(request):
    min = request.GET['min']  #doubt need explanation from Ma'am
    max = request.GET['max']
    # print(min)
    # print(max)
    q1 = Q(price__gte = min)
    q2 = Q(price__lte = max)
    q3 = Q(is_active = True)

    p = product.objects.filter(q1 & q2 & q3)
    context = {}
    context['products'] = p
    return render(request, 'index.html', context)

def addtocart(request, pid):
    userid = request.user.id
    u = User.objects.filter(id = userid)
    print(u[0])
    p = product.objects.filter(id = pid)
    print(p[0])

    q1 = Q(uid = u[0])
    q2 = Q(pid = p[0])
    c = cart.objects.filter(q1 and q2)
    n = len(c)
    print(n)
    context = {}
    context['products'] = p
    
    if n == 1:
        context['msg'] = "Product Already exists in the cart"
    else:
        c = cart.objects.create(uid = u[0], pid = p[0])
        c.save()
        
        context['success'] = "Product added Successfully in the cart !!!"
        
    # print(pid)
    # print(userid)
    return render(request, 'product_details.html', context)


def viewcart(request):
    if request.user.is_authenticated:
        userid = request.user.id
        c = cart.objects.filter(uid = userid)
        # print(c)
        # print(c[0].uid)
        # print(c[0].pid.name)
        # print(c[1].pid.name)
        # print(c[0].uid.is_superuser)
        # print(len(c))
        s = 0
        for i in c:
            # print(i)
            # print(i.pid.price)
            s = s + (i.pid.price * i.qty)

        np = len(c)

        context = {}
        context['products'] = c
        context['totalprice'] = s
        context['totalitem'] = np
        return render(request, 'cart.html', context)
    else:
        return redirect('/login')

def remove(request, cid):
    c = cart.objects.filter(id = cid)
    c.delete()

    return redirect('/viewcart')


def updateqty(request, qv, cid):
    c = cart.objects.filter(id = cid)
    # print(c[0].pid)
    # print(c[0].qty)
    
    if qv == "1":
      newqty  = c[0].qty + 1
      c.update(qty = newqty)
    else:
        if c[0].qty > 1:
            newqty = c[0].qty - 1
            c.update(qty = newqty)
    return redirect('/viewcart')


def placeorder(request):
    userid = request.user.id
    # print(userid)
    c = cart.objects.filter(uid = userid)
    # print(c)

    oid = random.randrange(1000, 9999)
    print(oid)

    for i in c:
        # print(i)
        # print(i.pid)
        # print(i.uid)
        # print(i.qty)
        o = order.objects.create(orderid = oid, pid = i.pid, uid = i.uid, qty = i.qty)
        o.save()  # shift data into order table
        i.delete()   # delete records from table

    orders = order.objects.filter(uid = userid)
    s = 0
    for i in orders:
        # print(i)
        # print(i.pid.price)
        s = s + (i.pid.price * i.qty)

    np = len(orders)

    context = {}
    context['products'] = orders
    context['totalprice'] = s
    context['totalitem'] = np

    return render(request, 'placeorder.html', context)
        

def makepayment(request):
    orders = order.objects.filter(uid = request.user.id)
    
    s = 0
    for i in orders:
        # print(i)
        # print(i.pid.price)
        s = s + (i.pid.price * i.qty)
        oid = i.orderid

    client = razorpay.Client(auth=("rzp_test_9TH7HLFyaq2ysI", "0ESpk0Atz5iu8kPVRe6QJNWL"))
    
    DATA = {
        "amount": s * 100,
        "currency": "INR",
        "receipt": oid,
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
    }
    payment = client.order.create(data = DATA)
    print(payment)
    context = {}
    context['data'] = payment
    client.order.create(data=DATA)
    
    # return HttpResponse(" in payment section ")
    return render(request, 'pay.html', context)