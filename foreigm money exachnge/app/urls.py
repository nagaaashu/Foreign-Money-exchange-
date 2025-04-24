from django.urls import path
from .views import *

urlpatterns = [
    path("updateTransaction/", view=updateTransaction, name="updateTransaction"),
    path("adminTransactions/", view=adminTransactions, name="adminTransactions"),
    path("transactions/", view=transactions, name="transactions"),
    path("addTransaction/", view=addTransaction, name="addTransaction"),
    path("exchanger/", view=exchanger, name="exchanger"),
    path("updateBalance/", view=updateBalance, name="updateBalance"),
    path("profile/", view=profile, name="profile"),
    path("updateCurrency/", view=updateCurrency, name="updateCurrency"),
    path("addCurrency/", view=addCurrency, name="addCurrency"),
    path("currencies/", view=currencies, name="currencies"),
    path("updateVerify/", view=updateVerify, name="updateVerify"),
    path("userHome/", view=userHome, name="userHome"),
    path("adminView/", view=adminView, name="adminView"),
    path("loginSubmit/", view=loginSubmit, name="loginSubmit"),
    path("signUpSubmit/", view=signUpSubmit, name="signUpSubmit"),
    path("adminLogin/", view=adminLogin, name="adminLogin"),
    path("", view=index, name=""),
    path("signup/", view=signup, name="signup"),
]
