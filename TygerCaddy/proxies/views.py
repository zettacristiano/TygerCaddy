from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Proxy, Header


class CreateProxy(LoginRequiredMixin, CreateView):
    template_name = 'proxies/add_proxy.html'
    model = Proxy
    success_url = '/proxies/list'
    fields = ['name',
              'proxy_from',
              'proxy_to',
              'load_policy',
              'fail_timeout',
              'max_fails',
              'max_conns',
              'try_duration',
              'try_interval',
              'health_check',
              'health_check_port',
              'health_check_interval',
              'health_check_timeout',
              'keep_alive',
              'timeout',
              'without',
              'exceptions',
              'insecure_skip_verify',
              'websocket',
              'transparent']


class ListProxies(LoginRequiredMixin, ListView):
    template_name = 'proxies/all_proxies.html'
    context_object_name = 'proxies'
    queryset = Proxy.objects.order_by('id')
    paginate_by = 10
    title = 'All Proxies'


class DetailProxy(LoginRequiredMixin, DetailView):
    template_name = 'proxies/proxy_detail.html'
    title = 'Proxy Detail'
    model = Proxy


class UpdateProxy(LoginRequiredMixin, UpdateView):
    model = Proxy
    fields = ['name',
              'proxy_from',
              'proxy_to',
              'load_policy',
              'fail_timeout',
              'max_fails',
              'max_conns',
              'try_duration',
              'try_interval',
              'health_check',
              'health_check_port',
              'health_check_interval',
              'health_check_timeout',
              'keep_alive',
              'timeout',
              'without',
              'exceptions',
              'insecure_skip_verify',
              'websocket',
              'transparent']
    slug_field = 'name'
    success_url = reverse_lazy('all-proxies')

    def form_valid(self, form):

        form.save()

        return redirect(reverse_lazy('all-proxies'))


class DeleteProxy(LoginRequiredMixin, DeleteView):
    model = Proxy
    title = "Delete Proxy"
    success_url = reverse_lazy('all-proxies')

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class CreateHeader(LoginRequiredMixin, CreateView):
    template_name = 'proxies/headers/add_header.html'
    model = Header
    success_url = '/proxies/headers/list'
    fields = ['header',
              'upstream',
              'downstream',
              'value',
              'proxy']


class ListHeaders(LoginRequiredMixin, ListView):
    template_name = 'proxies/headers/all_headers.html'
    context_object_name = 'headers'
    queryset = Header.objects.all()
    paginate_by = 10
    title = 'All Headers'


class DetailHeader(LoginRequiredMixin, DetailView):
    template_name = 'proxies/headers/header_detail.html'
    title = 'Header Detail'
    model = Proxy


class UpdateHeader(LoginRequiredMixin, UpdateView):
    model = Header
    fields = ['header',
              'upstream',
              'downstream',
              'value',
              'proxy']
    slug_field = 'header'
    success_url = reverse_lazy('all-headers')

    def form_valid(self, form):

        form.save()

        return redirect(reverse_lazy('all-headers'))


class DeleteHeader(LoginRequiredMixin, DeleteView):
    model = Header
    title = "Delete Header"
    success_url = reverse_lazy('all-headers')

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())