from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import *


admin.site.register(Edit)
admin.site.register(AHJ, SimpleHistoryAdmin)
admin.site.register(Address, SimpleHistoryAdmin)
admin.site.register(Location, SimpleHistoryAdmin)
admin.site.register(Contact, SimpleHistoryAdmin)
admin.site.register(EngineeringReviewRequirement, SimpleHistoryAdmin)
admin.site.register(User)
