from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, RedirectView
from .forms import StudentRegistration
from .models import User
from django.views import View
# Create your views here.

# This class will add item and show all items 
class UserAddShowView(TemplateView):
    template_name = 'enroll/addandshow.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StudentRegistration()
        context['stu'] = User.objects.all()
        return context
    
    def post(self, request):
        form = StudentRegistration(request.POST)
        if form.is_valid():
            nm = form.cleaned_data['name']
            em = form.cleaned_data['email']
            pw = form.cleaned_data['password']
            reg = User(name=nm, email=em, password=pw)
            reg.save()
            return HttpResponseRedirect('/thanks/')
        


# Landing Page for httpresopnseredirect
def thanks(request):
    return render(request, 'enroll/thanks.html')


# This class will Edit and update 
class UserUpdateView(View):
    def get(self, request, id):
        pi = User.objects.get(pk=id)
        fm = StudentRegistration()
        return render(request, 'enroll/updatestudent.html', {'form':fm})
    
    def post(self, request, id):
        pi = User.objects.get(pk=id)
        fm = StudentRegistration(request.POST, instance=pi)
        if fm.is_valid():
            # fm.save()
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['email']
            pw = fm.cleaned_data['password']
            upd = User(id=id, name=nm, email=em, password=pw)
            upd.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'enroll/updatestudent.html', {'form':fm})
    



# This class will Delete 
class UserDeleteView(RedirectView):
    url = '/'
    def get_redirect_url(self, *args, **kwargs):
        del_id = kwargs['id']
        User.objects.get(pk=del_id).delete()
        return super().get_redirect_url(*args, **kwargs)

