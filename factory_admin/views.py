from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Material, Inventory, DimensionConfig
from accounts.models import Design
from .forms import MaterialForm, InventoryForm, DimensionConfigForm

def is_factory_admin(user):
    return user.is_authenticated and user.is_staff

def admin_login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user and user.is_staff:
            login(request, user)
            return redirect('factory_admin:dashboard')
        else:
            messages.error(request, 'Invalid credentials or you do not have admin access.')
    return render(request, 'factory_admin/login.html')

def admin_logout_view(request):
    logout(request)
    return redirect('factory_admin:login')

@user_passes_test(is_factory_admin, login_url='factory_admin:login')
def dashboard_view(request):
    total_requests = Design.objects.count()
    recent_requests = Design.objects.order_by('-created_at')[:5]
    materials = Material.objects.all()
    inventory_items = Inventory.objects.select_related('material').all()
    
    # Low stock alert: less than 50
    low_stock_alerts = inventory_items.filter(quantity__lt=50)

    context = {
        'total_requests': total_requests,
        'recent_requests': recent_requests,
        'materials': materials,
        'inventory_items': inventory_items,
        'low_stock_alerts': low_stock_alerts,
    }
    return render(request, 'factory_admin/dashboard.html', context)

@user_passes_test(is_factory_admin, login_url='factory_admin:login')
def materials_view(request):
    materials = Material.objects.all()
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material added successfully.')
            return redirect('factory_admin:materials')
    else:
        form = MaterialForm()
        
    context = {'materials': materials, 'form': form}
    return render(request, 'factory_admin/materials.html', context)

@user_passes_test(is_factory_admin, login_url='factory_admin:login')
def delete_material_view(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Material deleted successfully.')
    return redirect('factory_admin:materials')

@user_passes_test(is_factory_admin, login_url='factory_admin:login')
def inventory_view(request):
    inventory_items = Inventory.objects.select_related('material').all()
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            material = form.cleaned_data['material']
            quantity = form.cleaned_data['quantity']
            # update or create
            inv, created = Inventory.objects.get_or_create(material=material)
            if created:
                inv.quantity = quantity
            else:
                inv.quantity += quantity
            inv.save()
            messages.success(request, 'Inventory updated successfully.')
            return redirect('factory_admin:inventory')
    else:
        form = InventoryForm()
    
    context = {'inventory_items': inventory_items, 'form': form}
    return render(request, 'factory_admin/inventory.html', context)

@user_passes_test(is_factory_admin, login_url='factory_admin:login')
def requests_view(request):
    requests = Design.objects.order_by('-created_at')
    context = {'requests': requests}
    return render(request, 'factory_admin/requests.html', context)

@user_passes_test(is_factory_admin, login_url='factory_admin:login')
def dimension_config_view(request):
    configs = DimensionConfig.objects.all()
    if request.method == 'POST':
        form = DimensionConfigForm(request.POST)
        if form.is_valid():
            # Update existing or create
            dt = form.cleaned_data['design_type']
            config, created = DimensionConfig.objects.update_or_create(
                design_type=dt,
                defaults={
                    'min_width': form.cleaned_data['min_width'],
                    'max_width': form.cleaned_data['max_width'],
                    'min_height': form.cleaned_data['min_height'],
                    'max_height': form.cleaned_data['max_height']
                }
            )
            messages.success(request, 'Dimension limits updated successfully.')
            return redirect('factory_admin:dimension_config')
    else:
        form = DimensionConfigForm()

    context = {'configs': configs, 'form': form}
    return render(request, 'factory_admin/dimension_config.html', context)
