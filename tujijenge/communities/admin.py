from django.contrib import admin

from .models import Community
admin.site.register(Community)

from .models import CommunityMember
admin.site.register(CommunityMember)

from .models import TrainingSession
admin.site.register(TrainingSession)

from .models import TrainingRegistration
admin.site.register(TrainingRegistration)
