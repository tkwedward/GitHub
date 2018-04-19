from django.conf.urls import url
from .views import home_page, input_page, source_table, table_form, detail_page, home_page, import_data, convert_to_json, add_tag, videoPage,  bulk_link_input, videoPageDetail, video_save

urlpatterns = [
    ####convert table into a form####
    url(r'^source$', source_table, name="source_table"),

    ####submit_the form####
    url(r'^submit$', table_form, name="form_submit"),

    ####scrape individual book####
    url(r'^input$', input_page, name="input_page"),

    url(r'^link_input$', bulk_link_input, name="link_input"),

    ####import data####
    url(r'^import$', import_data, name="import_page"),

    ####home page####
    url(r'^video_home$', videoPage, name="videoPage"),
    url(r'^video_home_detail$', videoPageDetail, name="videoPageDetail"),
    url(r'^video_save$', video_save, name="video_save"),


    url(r'^home$', home_page, name="home_page"),
    url(r'^home/(?P<tag>(.*))$', home_page, name="home_page_tag"),

    ####detail page####
    url(r'^detail/(?P<slug>\d+)$', detail_page, name="detail_page"),

    ####export data####
    url(r'^export$', convert_to_json, name="export"),

    url(r'^test$', add_tag, name="test"),



]
