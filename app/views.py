from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import EngineReport, EngineReportImage
from django.contrib.staticfiles import finders
from django.conf import settings
import os
import io
from xhtml2pdf import pisa

def report_form_view(request):
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        report = EngineReport.objects.create(
            service_report_no=data['service_report_no'],
            work_order_number=data['work_order_number'],
            vessel=data['vessel'],
            owner_agent=data['owner_agent'],
            imo_no=data['imo_no'],
            location=data['location'],
            equipment_type=data['equipment_type'],
            installation_type=data['installation_type'],
            engineer=data['engineer'],
            reason_for_call=data['reason_for_call'],
            job_description=data['job_description'],
        )

        # Save each uploaded image
        for img in images:
            EngineReportImage.objects.create(report=report, image=img)

        context = {"report": report}

        def link_callback(uri, rel):
            if uri.startswith(settings.MEDIA_URL):
                return os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
            elif uri.startswith(settings.STATIC_URL):
                return finders.find(uri.replace(settings.STATIC_URL, ''))
            return uri

        html = render_to_string("predefined_template.html", context)
        result = io.BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=result, link_callback=link_callback)

        if pisa_status.err:
            return HttpResponse("PDF generation error", status=500)

        result.seek(0)
        response = HttpResponse(result, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{report.service_report_no}.pdf"'
        return response

    return render(request, 'report_form.html')
