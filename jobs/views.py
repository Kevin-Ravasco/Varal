from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView


from .models import MicroTask, AllocatedJob
from .utils import send_job_allocation_email


@method_decorator(login_required, name='dispatch')
class JobsListView(ListView):
    queryset = MicroTask.objects.filter(is_selected=True, is_allocated=False).order_by('-timestamp')
    template_name = 'index.html'
    paginate_by = 6

    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        is_paginated = True if paginator.num_pages > 1 else False
        page_number = self.request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)
        return paginator, page_number, page_obj, is_paginated

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        pagination = self.paginate_queryset(self.get_queryset(), self.paginate_by)
        context['page_obj'] = pagination[2]
        context['is_paginated'] = pagination[3]
        return context

    def post(self, *args, **kwargs):
        user = self.request.user
        with transaction.atomic():
            microtask = get_object_or_404(MicroTask.objects.select_for_update(), id=self.request.POST.get('job_id'))
            if microtask.is_allocated:
                messages.error(self.request, 'Sorry, the selected task has already been allocated')
                return redirect(reverse('home'))
            else:
                AllocatedJob.objects.create(user=user, job=microtask, outsource_email=user.email)
                microtask.is_allocated = True
                microtask.save()
                current_site = get_current_site(self.request)
                send_job_allocation_email(user=user.profile, job=microtask, to_email=user.email, site=current_site)
                return redirect(reverse('jobs_confirmation'))





