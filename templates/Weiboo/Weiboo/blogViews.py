from django.shortcuts import render

def contact(request):     
      data = {
       'title':'Contact',
       'subTitle':'Contact',
       'subTitle2':'Contact',
       'css': '<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
       'footer':'true',
      }
      return render(request, "blog/contact.html", data)

def news(request):     
      data = {
       'title':'News',
       'subTitle':'Blog',
       'subTitle2':'News',
       'footer':'true',
      }
      return render(request, "blog/news.html", data)

def newsDetails(request):     
      data = {
       'title':'News Details',
       'subTitle':'Blog',
       'subTitle2':'News Details',
       'footer':'true',
      }
      return render(request, "blog/newsDetails.html", data)

def newsGrid(request):     
      data = {
       'title':'News-Grid',
       'subTitle':'Blog',
       'subTitle2':'News-Grid',
       'footer':'true',
      }
      return render(request, "blog/newsGrid.html", data)