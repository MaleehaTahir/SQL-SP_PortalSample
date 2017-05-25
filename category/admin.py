from django.contrib import admin

from category import models as category_models


class CategoryAdmin(admin.ModelAdmin):

	class Meta:
		model = category_models.Category


class SubCategoryAdmin(admin.ModelAdmin):

	class Meta:
		model = category_models.SubCategory


class ReportAdmin(admin.ModelAdmin):

	class Meta:
		model = category_models.Report


class ReportProcedureAdmin(admin.ModelAdmin):

	class Meta:
		model = category_models.ReportProcedure


admin.site.register(category_models.Category, CategoryAdmin)
admin.site.register(category_models.SubCategory, SubCategoryAdmin)
admin.site.register(category_models.Report, ReportAdmin)
admin.site.register(category_models.ReportProcedure, ReportProcedureAdmin)
admin.site.register(category_models.Filter)
admin.site.register(category_models.ReportFilter)
