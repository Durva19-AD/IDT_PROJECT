from django.db import models
from django.conf import settings

class Design(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    typology = models.CharField(max_length=50)
    width = models.FloatField()
    height = models.FloatField()
    quantity = models.IntegerField()
    material = models.CharField(max_length=50)
    total_cost = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.typology} ({self.width}x{self.height}) by {self.user}"

    def clean(self):
        from django.core.exceptions import ValidationError
        from factory_admin.models import DimensionConfig
        
        try:
            config = DimensionConfig.objects.get(design_type=self.type)
            if self.width < config.min_width or self.width > config.max_width:
                raise ValidationError({
                    'width': f"Width must be between {config.min_width} mm and {config.max_width} mm for {self.type}s."
                })
            if self.height < config.min_height or self.height > config.max_height:
                raise ValidationError({
                    'height': f"Height must be between {config.min_height} mm and {config.max_height} mm for {self.type}s."
                })
        except DimensionConfig.DoesNotExist:
            pass # No config defined for this type, skip validation
