from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, WeightForm
from .models import Weight

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=password)
            # login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_form(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('weight_list')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
@login_required
def add_weight(request):
    if request.method == 'POST':
        form = WeightForm(request.POST)
        if form.is_valid():
            weight_instance = form.save(commit=False)
            weight_instance.user = request.user
            try:
                weight_instance.save()
                return redirect('weight_list')
            except:
                form.add_error(None, "You can only add one weight entry per day.")
    else:
        form = WeightForm()
    return render(request, 'add_weight.html', {'form': form})

@login_required
def weight_list(request):
    weights = Weight.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(weights, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'weight_list.html', {'page_obj': page_obj})

@login_required
def edit_weight(request, pk):
    weight = Weight.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = WeightForm(request.POST, instance=weight)
        if form.is_valid():
            form.save()
            return redirect('weight_list')
    else:
        form = WeightForm(instance=weight)
    return render(request, 'edit_weight.html', {'form': form})

# @login_required
# def delete_weight(request, pk):
#     weight = Weight.objects.get(pk=pk, user=request.user)
#     if request.method == 'POST':
#         weight.delete()
#         return redirect('weight_list')
#     return render(request, 'delete_weight.html', {'weight': weight})

@login_required
def delete_weight(request, pk):
    if request.method == 'POST':
        try:
            weight = Weight.objects.get(id=pk, user=request.user)
            weight.delete()
            return JsonResponse({'success': True})
        except Weight.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Weight entry not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

@login_required
def weight_loss(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    weight_entries = Weight.objects.filter(user=request.user, date__range=[start_date, end_date]).order_by('date')
    if weight_entries.exists():
        weight_loss = weight_entries.first().weight - weight_entries.last().weight
        return JsonResponse({'weight_loss': weight_loss})
    return JsonResponse({'error': 'No entries found in this date range'})

def logout(request):
    auth_logout(request)
    return redirect('login')