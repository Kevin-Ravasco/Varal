from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView


from jobs.models import AllocatedJob


@method_decorator(login_required, name='dispatch')
class ProfileView(ListView):
    template_name = 'profile.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = AllocatedJob.objects.filter(user=self.request.user).select_related('job').order_by('-time_allocated')
        return queryset

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
        allocation_id = self.request.POST.get('allocation_id')
        AllocatedJob.objects.filter(id=allocation_id).update(time_completed=timezone.now())
        return redirect(reverse('account_profile'))






