from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Product
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects
    return render(request, 'products/home.html',{'products':products})

@login_required(login_url="signup")
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view

class CreateProduct(generic.CreateView):
    model = Product
    fields = ['title', 'description', 'body', 'url', 'image', 'icon']
    template_name = 'products/create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateProduct, self).form_valid(form)
        return redirect('home')

class ViewProduct(generic.DetailView):
    model = Product
    template_name = 'products/view.html'
