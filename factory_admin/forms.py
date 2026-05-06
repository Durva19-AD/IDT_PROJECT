from django import forms
from .models import Material, Inventory

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'price_per_unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Aluminium'}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['material', 'quantity']
        widgets = {
            'material': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
        }

from .models import DimensionConfig
class DimensionConfigForm(forms.ModelForm):
    class Meta:
        model = DimensionConfig
        fields = ['design_type', 'min_width', 'max_width', 'min_height', 'max_height']
        widgets = {
            'design_type': forms.Select(attrs={'class': 'form-select'}),
            'min_width': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'max_width': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'min_height': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'max_height': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
        }
