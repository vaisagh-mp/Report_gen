from django.db import models

class EngineReport(models.Model):
    service_report_no = models.CharField(max_length=100)
    work_order_number = models.CharField(max_length=100)
    vessel = models.CharField(max_length=100)
    owner_agent = models.CharField(max_length=100)
    imo_no = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=100)
    installation_type = models.CharField(max_length=100)
    engineer = models.CharField(max_length=100)
    reason_for_call = models.TextField()
    job_description = models.TextField()

    def __str__(self):
        return self.service_report_no


class EngineReportImage(models.Model):
    report = models.ForeignKey(EngineReport, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='report_images/')
