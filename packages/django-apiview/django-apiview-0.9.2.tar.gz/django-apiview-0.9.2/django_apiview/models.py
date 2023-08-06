
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ApiResponseTimeLog(models.Model):
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Add Time"))
    path = models.CharField(max_length=128, verbose_name=_("Api Path"))
    response_time = models.IntegerField(verbose_name=_("Response Time"), help_text=_("Response time in microsecond. 1,000,000 microseconds == 1 second."))

    class Meta:
        verbose_name = _("Api Response Time Log")
        verbose_name_plural = _("Api Response Time Logs")

    def __str__(self):
        return str(self.pk)
