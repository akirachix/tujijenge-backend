from django.contrib import admin

from .models import Community
admin.site.register(Community)

from .models import CommunityMembers
admin.site.register(CommunityMembers)

from .models import TrainingSessions
admin.site.register(TrainingSessions)

from .models import TrainingRegistration
admin.site.register(TrainingRegistration)