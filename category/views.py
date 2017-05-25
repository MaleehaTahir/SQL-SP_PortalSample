from collections import OrderedDict
import datetime
import xlwt

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.db import connection
from django.utils.dateparse import parse_date

from category.models import Category, SubCategory, Report, ReportProcedure


DB_DATE_FORMAT = '%Y%m%d'


def get_list_of_categories(request):

    categories = Category.objects.all()
    context = {'categories': categories}

    return render(request, 'categories.html', context)


def get_list_of_sub_categories(request):
    context = {}
    try:
        category = Category.objects.get(id=request.GET['category_id'])
        sub_categories = category.sub_category.all()
        context = {'sub_categories': sub_categories}
        return render(request, 'sub_categories.html', context)
    except:
        print ("Wrong category ID")

    return render(request, 'sub_categories.html', context)


def get_reports_for_sub_categories(request):
    context = {}
    try:
        sub_category = SubCategory.objects.get(id=request.GET['sub_category_id'])
        reports = sub_category.report.all()
        context = {'reports': reports}
    except:
        print ("Wrong sub category ID")

    return render(request, 'reports.html', context)


def get_report_detail(request, report_id):
    report = Report.objects.get(id=report_id)
    report_procedure = report.reportprocedure_set.first()

    context = {
        'report': report,
        'Procedure_Name': report_procedure
    }
    conn = None

    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(weeks=6)
    sql_params = []
    filters = OrderedDict()

    if 'start_date' in request.GET:
        start_date = parse_date(request.GET['start_date'])

    if 'end_date' in request.GET:
        end_date = parse_date(request.GET['end_date'])

    sql_params.append(start_date.strftime(DB_DATE_FORMAT))
    sql_params.append(end_date.strftime(DB_DATE_FORMAT))

    # Configurable filters
    for report_filter in report_procedure.reportfilter_set.all().order_by('parameter_position'):
        filter_name = report_filter.filter.name
        filter_value = ''
        if filter_name in request.GET:
            filter_value = request.GET[filter_name]
            sql_params.append(filter_value)
        filters[filter_name] = filter_value
    context['filters'] = filters

    try:
        conn = connection.cursor()  # connection established

        # Make placeholders for as many params as we have
        params_placeholders = ['%s'] * len(sql_params)
        params_sql = ', '.join(params_placeholders)

        # Default to Azure SQL
        sql = "EXEC %s %s"  # double percents on params to sql call
        if settings.DATABASES['default']['ENGINE'].endswith('mysql'):
            # Use MySQL if it's set up
            sql = "call %s (%s)"
        sql = sql % (report_procedure.name, params_sql)
        print(sql)
        print(sql_params)

        conn.execute(sql, params=sql_params)

        context['field_names'] = [i[0] for i in conn.description]

        rows = conn.fetchall()
        context['rows'] = rows
        context['report_id'] = int(report_id)

        # Download the report as excel
        if 'export' in request.GET:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="report.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Reports')

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            font_style.width = int(13*260)
            font_style.alignment.horz = font_style.alignment.HORZ_CENTER

            columns = ['column_1', 'column_2', 'column_3', 'column_4', 'column_5', 'column_6', ]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            ws.col(1).width = len('column_2') * 300
            ws.col(5).width = len('column_5') * 256

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    if isinstance(row[col_num], datetime.date):
                        row_col_date = row[col_num].strftime("%Y-%m-%d")
                        content_format   = 'align: wrap on'
                        ws.write(row_num, col_num, row_col_date, font_style)
                    else:
                        ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)
            return response

    except Exception as e:
        print(e)
        print("No report object found")
    finally:
        if conn:
            conn.close()  # closing the connection

    context['start_date'] = start_date
    context['end_date'] = end_date
    print(context)
    return render(request, 'report_detail.html', context)


def get_report_detail_mssql(request, report_id):
    print(report_id)
    report = Report.objects.get(id=int(report_id))
    report_procedure = ReportProcedure.objects.get(report=report)
    end_date = datetime.datetime.now().date()
    start_date = datetime.datetime.now().date() - datetime.timedelta(weeks=1)
    if 'start_date' in request.GET and 'end_date' in request.GET:
        print('in if')
        start_date = parse_date(request.GET['start_date'])
        end_date = parse_date(request.GET['end_date'])

    print(start_date)
    print(type(end_date))
    conn = connection.cursor()
    sql = "EXEC %s %s, %s"
    conn.execute(sql, params=(report_procedure.name,
                              start_date.strftime(DB_DATE_FORMAT),
                              end_date.strftime(DB_DATE_FORMAT)))
    rows = conn.fetchall()
    context = {"rows": rows}
    context['report_id'] = int(report_id)
    # Download as Excel Report
    if 'export' in request.GET:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Reports')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.width = int(13 * 260)
        font_style.alignment.horz = font_style.alignment.HORZ_CENTER

        columns = ['Date Key', 'Location Number', 'Total Units', 'Total Value', 'S Number', 'Product Description', ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        ws.col(1).width = len('Location Number') * 300
        ws.col(5).width = len('Product Description') * 256

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                if isinstance(row[col_num], datetime.date):
                    row_col_date = row[col_num].strftime("%Y-%m-%d")
                    content_format = 'align: wrap on'
                    ws.write(row_num, col_num, row_col_date, font_style)
                else:
                    ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    conn.close()  # closing the connection

    return render(request, 'report_detail.html', context)