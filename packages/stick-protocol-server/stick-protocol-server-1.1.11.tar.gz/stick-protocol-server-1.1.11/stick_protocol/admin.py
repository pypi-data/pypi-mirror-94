from django.contrib import admin

from .models import IdentityKey, SignedPreKey, PreKey, EncryptingSenderKey, DecryptingSenderKey, Party

admin.site.register(IdentityKey)
admin.site.register(SignedPreKey)
admin.site.register(PreKey)
admin.site.register(EncryptingSenderKey)
admin.site.register(DecryptingSenderKey)
admin.site.register(Party)