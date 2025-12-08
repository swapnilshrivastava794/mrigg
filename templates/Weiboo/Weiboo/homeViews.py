from django.shortcuts import render

def allCategory(request):     
      data = {
       'title':'All Catagory',
       'subTitle':'Home',
       'subTitle2':'All Catagory',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
      }
      return render(request, "home/allCategory.html", data)

def category(request):     
      data = {
       'title':'Catagory',
       'subTitle':'Home',
       'subTitle2':'Catagory',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/jquery.nstSlider.min.css"/> <link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
      }
      return render(request, "home/category.html", data)

def externalProducts(request):     
      data = {
       'title':'External Product',
       'subTitle':'Home',
       'subTitle2':'External Product',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/jquery.nstSlider.min.css"/> <link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
      }
      return render(request, "home/externalProducts.html", data)

def index(request):     
      data = {
       'header':'flase',
       'footer':'true',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable1.css"/>',
      }
      return render(request, "home/index.html", data)

def indexEight(request):     
      data = {
       'header':'flase',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable4.css"/>',
      }
      return render(request, "home/indexEight.html", data)

def indexFive(request):     
      data = {
       'header':'flase',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable4.css"/>',
      }
      return render(request, "home/indexFive.html", data)

def indexFour(request):     
      data = {
       'header':'flase',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable3.css"/>',
      }
      return render(request, "home/indexFour.html", data)

def indexNine(request):     
      data = {
       'header':'flase',
       'footer':'true',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable1.css"/>',
      }
      return render(request, "home/indexNine.html", data)

def indexSeven(request):     
      data = {
       'header':'flase',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable7.css"/>',
      }
      return render(request, "home/indexSeven.html", data)

def indexSix(request):     
      data = {
       'header':'flase',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable5.css"/>',
      }
      return render(request, "home/indexSix.html", data)

def indexTen(request):     
      data = {
       'header':'flase',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable10.css"/>',
      }
      return render(request, "home/indexTen.html", data)

def indexThree(request):     
      data = {
       'header':'flase',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable2.css"/>',
      }
      return render(request, "home/indexThree.html", data)

def indexTwo(request):     
      data = {
       'header':'flase',
       'footer':'true',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable1.css"/>',
      }
      return render(request, "home/indexTwo.html", data)

def login(request):     
      data = {
       'title':'Log In',
       'subTitle':'Home',
       'subTitle2':'Log In',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
      }
      return render(request, "home/login.html", data)

def outOfStockProducts(request):     
      data = {
       'title':'Out Of Stock',
       'subTitle':'Home',
       'subTitle2':'Out Of Stock',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
      }
      return render(request, "home/outOfStockProducts.html", data)

def shopFiveColumn(request):     
      data = {
       'title':'Shop Five Column',
       'subTitle':'Home',
       'subTitle2':'Shop Five Column',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable1.css"/> <link rel="stylesheet" type="text/css" href="/static/css/jquery.nstSlider.min.css"/>',
      }
      return render(request, "home/shopFiveColumn.html", data)

def simpleProducts(request):     
      data = {
       'title':'Simple Products',
       'subTitle':'Home',
       'subTitle2':'Simple Products',
      }
      return render(request, "home/simpleProducts.html", data)

def thankYou(request):     
      data = {
       'title':'Thank You',
       'subTitle':'Home',
       'subTitle2':'Thank You',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable1.css"/>',
      }
      return render(request, "home/thankYou.html", data)

def wishlist(request):     
      data = {
       'title':'Thank You',
       'subTitle':'Home',
       'subTitle2':'Thank You',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable1.css"/>',
      }
      return render(request, "home/wishlist.html", data)
