from django.shortcuts import render

def about(request):     
      data = {
       'title':'About',
       'subTitle':'Pages',
       'subTitle2':'About',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
       'footer':'true',
      }
      return render(request, "pages/about.html", data)

def errorPage(request):     
      data = {
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
       'footer':'true',
      }
      return render(request, "pages/errorPage.html", data)

def faq(request):     
      data = {
       'title':'Faq',
       'subTitle':'Pages',
       'subTitle2':'Faq',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable1.css"/>',
       'footer':'true',
      }
      return render(request, "pages/faq.html", data)