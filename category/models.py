from __future__ import unicode_literals

from django.db import models


class Report(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return self.__unicode__()


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    report = models.ManyToManyField(Report, blank=True)

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return self.__unicode__()


class Category(models.Model):
    name = models.CharField(max_length=255)
    sub_category = models.ManyToManyField(SubCategory, blank=True)

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return self.__unicode__()


class Filter(models.Model):
    name = models.CharField(max_length=255)
    # This may also need type (e.g. int or string)

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return self.__unicode__()


class ReportProcedure(models.Model):
    name = models.CharField(max_length=255)
    report = models.ForeignKey(Report)

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return self.__unicode__()


class ReportFilter(models.Model):
    filter = models.ForeignKey(Filter)
    report_procedure = models.ForeignKey(ReportProcedure)
    parameter_position = models.IntegerField()

    class Meta:
        unique_together = ('filter', 'report_procedure', 'parameter_position')

    def __unicode__(self):
        return "%s by %s" % (self.report_procedure, self.filter)

    def __str__(self):
        return self.__unicode__()
