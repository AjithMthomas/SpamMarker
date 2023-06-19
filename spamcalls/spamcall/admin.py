from django.contrib import admin
from . models import User,Contact,SpamNumber,SearchHistory

# Register your models here.
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(SpamNumber)
admin.site.register(SearchHistory)