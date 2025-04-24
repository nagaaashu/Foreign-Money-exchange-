from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.db.models import Q
from django.http.response import JsonResponse
from web3 import Web3
import json
from datetime import datetime

def updateTransaction(request):
    if request.method=="POST":
        transaction_id=request.POST.get('transaction_id',0)
        action=request.POST.get('action','')
        crr=request.POST.get('crr','')
        print(crr)
        contractDetails.functions.updateStatus(int(transaction_id),crr+"&*&*"+action).transact(one)
        return redirect('adminTransactions')

def adminTransactions(request):
    data = []
    ids, userids, amounts, statuses, dateValues = contractDetails.functions.getUsers().call(
        one
    )
    for i in range(len(ids)):
        view=statuses[i].split("&*&*")
        data.append(
                {
                    "id": ids[i],
                    "userids": userids[i],
                    "amounts": amounts[i],
                    "statuses":view[1],
                    "currency":view[0],
                    "dateValues": dateValues[i],
                }
            )
    return render(request, "adminPoint/history.html", context={"data":data})

def transactions(request):
    if request.method == "GET":
        id = request.GET.get("id", 0)

        data = []
        ids, userids, amounts, statuses, dateValues = contractDetails.functions.getUsers().call(
            one
        )
        for i in range(len(ids)):
            print(userids)
            if int(id) == userids[i]:
                view=statuses[i].split("&*&*")
                data.append(
                    {
                        "id": ids[i],
                        "userids": userids[i],
                        "amounts": amounts[i],
                        "statuses":view[1],
                        "currency":view[0],
                        "dateValues": dateValues[i],
                    }
                )

    return render(request, "user/history.html", context={"data":data})


one = {"from": "0xc7Da9efc3C66762d001ba37379A9D9894DEa30aB"}
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

with open("0 blocks/build/contracts/Transaction.json") as f:
    contractDetails = web3.eth.contract(
        address="0x1C2C0b65187a302B4a224c38134AeAEA662b96E4", abi=json.load(f)["abi"]
    )


def addTransaction(request):
    amount = request.POST.get("amount", "")
    id = request.POST.get("id", 0)
    option = request.POST.get("option", "").strip()
    data = option.split(",")
    now = datetime.now()
    txt = now.strftime("%Y-%m-%d %H:%M:%S")
    contractDetails.functions.addPress(
        int(id), int(amount), str(data[1] + "&*&*"+"Pending"), str(txt)
    ).transact(one)
    messages.info(request, "Transaction SuccessFully!!")

    return redirect("currencies")


def exchanger(request):
    name = CurrencyRate.objects.filter().values("name", "exRate", "id")
    return render(request, "user/exchanger.html", context={"currency": name})


def updateBalance(request):
    if request.method == "POST":
        id = request.POST.get("id", 0)
        balance = request.POST.get("bal", 0)
        user = Users.objects.filter(id=int(id)).last()

        user.balance = user.balance + int(balance)
        user.save()
    return redirect("userHome")


def profile(request):
    if request.method == "GET":
        id = request.GET.get("id", "")
        rate = Users.objects.filter(id=id).last()
        return JsonResponse(
            {
                "fname": rate.uname,
                "email": rate.email,
                "uname": rate.uname,
                "check": rate.checkPoint,
                "balance": rate.balance,
                "crr": rate.curr,
            }
        )


def updateCurrency(request):
    if request.method == "POST":
        crn = request.POST.get("crn", "").strip()
        id = request.POST.get("id", 0)
        exRate = request.POST.get("exRate", "").strip()
        cur = CurrencyRate.objects.filter(id=int(id)).last()
        cur.name = crn
        cur.exRate = exRate
        cur.save()
    return redirect("currencies")


def addCurrency(request):
    if request.method == "POST":
        name2 = request.POST.get("name", "").strip()
        exRate2 = request.POST.get("exRate", "").strip()
        if CurrencyRate.objects.filter(name=name2).exists():
            messages.error(request, "Try with another Currency name")
            return redirect("currencies")
        else:
            CurrencyRate.objects.create(exRate=exRate2, name=name2)
            return redirect("currencies")


def currencies(request):
    data = CurrencyRate.objects.filter().values("name", "exRate", "id")
    return render(request, "adminPoint/currencies.html", context={"currency": data})


def updateVerify(request):
    if request.method == "POST":
        id = request.POST.get("id", "").strip()
        status = request.POST.get("status", "").strip()
        user = Users.objects.filter(id=int(id)).last()
        user.checkPoint = status
        user.save()
        return redirect("adminView")


def userHome(request):
    rate = CurrencyRate.objects.filter().values("name", "exRate")
    return render(request, "user/index.html", context={"currency": rate})


def adminView(request):
    pending = Users.objects.filter(checkPoint="Pending").values(
        "fname", "email", "uname", "curr", "id"
    )
    blocked = Users.objects.filter(checkPoint="Blocked").values(
        "fname", "email", "uname", "curr", "id"
    )
    verified = Users.objects.filter(checkPoint="Verified").values(
        "fname", "email", "uname", "curr", "id"
    )

    return render(
        request,
        "adminPoint/index.html",
        context={"pending": pending, "blocked": blocked, "verified": verified},
    )


def loginSubmit(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        check = Users.objects.filter(
            Q(email=username) | Q(uname=username), password=password
        ).last()
        if check is None:
            messages.error(request, "Invalid User!!")
            return redirect("")
        else:

            if check.checkPoint == "Pending":
                messages.error(request, "Need to Verify your Account !!")
            elif check.checkPoint == "Blocked":
                messages.error(request, "Sorry Your Account is Blocked")
            else:
                messages.success(request, "Login Successuflly !!")
                messages.info(request, f"{check.id}")
                return redirect("userHome")

    return redirect("")


def signUpSubmit(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname", "").strip()
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        option = request.POST.get("option", "").strip()
        print(option)
        if Users.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exists !!")
            return redirect("signup")
        else:
            Users.objects.create(
                fname=fullname,
                email=email,
                password=password,
                uname=username,
                checkPoint="Pending",
                curr=option,
            )
            messages.error(request, "Success Registered !!")
            return redirect("")


def adminDashBoard(request):
    return render(request, "")


def index(request):
    return render(request, "index.html")


def adminLogin(request):

    return render(request, "adminLogin.html")


def signup(request):
    name = CurrencyRate.objects.filter().values("name")
    return render(request, "signup.html", context={"name": name})
