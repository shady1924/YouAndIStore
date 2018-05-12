from django.conf.urls import url
from empTimeSheet import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='index'),
    url(r'^uploadexcel$', views.uploadExcel, name='uploadexcel'),
    url(r'^saveexcel/$', views.readAndSaveExcelData, name='saveexcel'),
    url(r'^retdata$', views.CheckRetData, name='retdata'),
    url(r'^detailmonthlyreport/$', views.detailMonthlyReport, name='detailmonthreport'),
    url(r'^saveStoreConfig/$', views.saveStoreConfig, name='savestoreconfig'),
    url(r'^salarySummary/$', views.getComputedSalaryData, name='salarysummary'),
    url(r'^getMonths/$', views.getMonths, name='getmonths'),

]