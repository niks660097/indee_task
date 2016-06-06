import os
import random
import string
from datetime import datetime, timedelta
from django.db import models

def decide_file_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class UserDocument(models.Model):
    DOCUMENT_TYPE = (('PDF', 0),
                     ('TEXT', 1))

    user = models.ForeignKey('auth.User')
    doc_type = models.IntegerField(choices=DOCUMENT_TYPE)
    doc = models.FileField(upload_to=decide_file_path)
    secure_link = models.TextField(blank=True, default='')
    date_uploaded = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_uploaded = datetime.now()
        super(UserDocument, self).save(*args, **kwargs)

    def generate_secure_link(self, save_to_inst=False):
        rand_choices = list(string.lowercase)
        rand_choices.extend(range(10))
        rand_link = ''.join(str(random.choice(rand_choices)) for x in range(10))
        while UserDocument.objects.filter(secure_link=rand_link).first():
                rand_link = ''.join(random.choice(rand_choices) for x in range(10))
        if save_to_inst:
            self.secure_link = rand_link
            self.save()
        return rand_link

    @property
    def filename(self):
       return os.path.basename(self.doc.name)
