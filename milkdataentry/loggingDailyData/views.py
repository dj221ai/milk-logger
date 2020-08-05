from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import EntryData, MonthlyMilkData, RatePerLitre
from .forms import EntryDataForm, RateForm
from django.conf import settings
from twilio.rest import Client


class HomePage(TemplateView):
    template_name = 'loggingDailyData/home.html'


# @transaction.atomic()
class EntryCreateView(LoginRequiredMixin, CreateView):
    form_class = EntryDataForm
    template_name = 'loggingDailyData/index.html'
    success_url = '/saved/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            daily_intake = form.cleaned_data.get('daily_intake')
            extra_intake = form.cleaned_data.get('extra_intake')
            print(daily_intake, extra_intake)
            if extra_intake is None:
                extra_intake = float(0.0)
                print(float(extra_intake))
            daily_milk_data = daily_intake+extra_intake
            daily_milk_data = float(daily_milk_data)
            print('daily_milk_data ', daily_milk_data)
            form.instance.user = self.request.user
            call_monthly_model = MonthlyMilkData.objects.create(user=form.instance.user,
                                                                total_monthly_milk=daily_milk_data)
            form.save()
            call_monthly_model.save()
            new_daily_milk_data = str(daily_milk_data)
            account_sid = 'your twilio account sid'
            auth_token = 'your twilio auth token'

            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_='number which twilio provided',
                body="Total milk given on {} August is {} ".format(date, new_daily_milk_data),
                to='number on which you want to send the message'
            )

            print('msg ', message.sid)
            return redirect('loggingDailyData:daily_total')
        return super(EntryCreateView, self).form_valid(form)


# you can also write the signal code for sending message for both create and update view


class EntryUpdateView(UpdateView):
    form_class = EntryDataForm
    template_name = 'loggingDailyData/index.html'
    queryset = EntryData.objects.all()
    success_url = reverse_lazy("loggingDailyData:daily_total")

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(EntryData, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(EntryUpdateView, self).form_valid(form)


class EntryDeleteView(DeleteView):
    model = EntryData
    template_name = 'loggingDailyData/entrydata_delete.html'
    success_url = reverse_lazy('loggingDailyData:daily_total')

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(EntryData, id=id_)


class DailyTotal(LoginRequiredMixin, ListView):
    model = EntryData
    ordering = ['date']
    template_name = 'loggingDailyData/daily_total.html'

    def get_queryset(self):
        return EntryData.objects.filter(user=self.request.user)


class SavedDisplay(LoginRequiredMixin, TemplateView):
    template_name = 'loggingDailyData/saved.html'


def monthly_milk(request):
    context = {}
    total_data = MonthlyMilkData.objects.all()
    total_list = []
    for i in total_data:
        each_data = i.total_monthly_milk
        print('each_data', each_data)
        total_list.append(each_data)
    total_list = sum(total_list)
    context['total_list'] = total_list
    return render(request, 'loggingDailyData/monthly_total_milk.html', context=context)

