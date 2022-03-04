from django.db import models
from django.utils.translation import gettext_lazy as _

from models.base import BaseModel


class Document(BaseModel):
    # All FK to momel
    open_innovation_submit = models.ForeignKey('main.OpenInnovationSubmit', on_delete=models.CASCADE, blank=True,
                                               null=True)
    open_innovation = models.ForeignKey('main.OpenInnovation', on_delete=models.CASCADE, blank=True, null=True)
    solution_report = models.ForeignKey('main.SolutionReport', on_delete=models.CASCADE, blank=True, null=True)
    user_activity = models.ForeignKey(to='main.UserActivity', on_delete=models.CASCADE, blank=True, null=True)
    user_certificate = models.ForeignKey(to='main.UserCertificate', on_delete=models.CASCADE, blank=True, null=True)
    user_scientific_research = models.ForeignKey(to='main.UserScientificResearch', on_delete=models.CASCADE,
                                                 blank=True, null=True)
    lecturer = models.ForeignKey(to='hSchool.Lecturer', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255, help_text=_('Name of document'))
    doc_file = models.FileField(max_length=None, upload_to='main/documents/%Y/%m/%d/', blank=True, null=True)
    description = models.CharField(max_length=255, help_text=_('Description'))

    class Meta:
        db_table = 'hinnox_document'
        verbose_name = _('Document')
        verbose_name_plural = _('Document')

    def __str__(self):
        return f'{self.name}'

    @property
    def get_full_path(self):
        if not self.doc_file:
            return None
        return self.doc_file.path

    @property
    def get_owner(self):
        return self.open_innovation_submit or self.open_innovation or self.solution_report\
               or self.user_activity or self.user_certificate or self.user_scientific_research or self.lecturer\
               or None


class DocumentVersion(BaseModel):
    document = models.ForeignKey(to=Document, on_delete=models.PROTECT, help_text=_('FK document'))
    version = models.FloatField(default=1.0, help_text=_('Version of document version'))

    class Meta:
        db_table = 'hinnox_document_version'
        verbose_name = _('Document version')
        verbose_name_plural = _('Document version')

    def __str__(self):
        return f'{self.document} - {self.version}'
