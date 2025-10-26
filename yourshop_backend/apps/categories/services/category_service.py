from apps.categories.models import Category

class CategoryService:
    def get_categories(self):
        return Category.objects.filter(parent__isnull=True).prefetch_related('children')