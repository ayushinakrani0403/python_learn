from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import JobSerializer
from .tasks import send_job_alert_email

class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        job = serializer.save(created_by=self.request.user)
        send_job_alert_email.delay(job.id)
