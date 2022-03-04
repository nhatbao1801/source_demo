#  Copyright (c) 2020.
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH
from datetime import datetime

from django.db import models

from hSchool.models import Course, Question, CourseQuestionAnswer
from models.message import Message
from models.report_type import ReportType


class Report(models.Model):
    reported_type = models.ForeignKey(to=ReportType, on_delete=models.CASCADE)
    who_reported = models.ForeignKey(to='main.User', related_name='reported_to', on_delete=models.CASCADE)
    user_being_reported = models.ForeignKey(to='main.User', related_name='was_reported', blank=True, null=True,
                                            on_delete=models.CASCADE)
    team = models.ForeignKey(to='main.Team', blank=True, null=True, on_delete=models.CASCADE)
    org = models.ForeignKey(to='main.Organization', blank=True, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(to='main.Event', blank=True, null=True, on_delete=models.CASCADE)
    contest = models.ForeignKey(to='main.Contest', blank=True, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(to='main.Post', blank=True, null=True, on_delete=models.CASCADE)
    job = models.ForeignKey(to='main.Job', blank=True, null=True, on_delete=models.CASCADE)
    job_freelance = models.ForeignKey(to='main.JobFreelance', blank=True, null=True, on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course, blank=True, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, blank=True, null=True, on_delete=models.CASCADE)
    course_qa = models.ForeignKey(to=CourseQuestionAnswer, blank=True, null=True, on_delete=models.CASCADE)
    message = models.ForeignKey(to=Message, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True, help_text='Tiêu để báo cáo')
    content = models.CharField(max_length=1000, blank=True, null=True, help_text='Nội dung báo cáo')
    date_created = models.DateTimeField(default=datetime.today)

    class Meta:
        db_table = 'hinnox_target_was_reported'
        verbose_name = 'đối tượng bị báo cáo'
        verbose_name_plural = 'TargetWasReported - Đối tượng bị báo cáo'

    def get_target(self) -> tuple:
        """
        :return: (target, type, reportype_level)
        """
        if self.user_being_reported is not None:
            return self.user_being_reported, 'user', self.reported_type.level
        if self.team is not None:
            return self.team, 'team', self.reported_type.level
        if self.org is not None:
            return self.org, 'org', self.reported_type.level
        if self.event is not None:
            return self.event, 'event', self.reported_type.level
        if self.contest is not None:
            return self.contest, 'contest', self.reported_type.level
        if self.post is not None:
            return self.post, 'post', self.reported_type.level
        if self.job is not None:
            return self.job, 'job', self.reported_type.level
        if self.job_freelance is not None:
            return self.job_freelance, 'job_freelance', self.reported_type.level
        if self.course is not None:
            return self.course, 'course', self.reported_type.level
        if self.question is not None:
            return self.question, 'question', self.reported_type.level
        if self.message is not None:
            return self.message, 'message', self.reported_type.level
