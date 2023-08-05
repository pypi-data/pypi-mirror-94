from django.apps import AppConfig
from . import __version__


class YfTemplatesConfig(AppConfig):
    name = "yf_templates"
    label = "yf_templates"
    verbose_name = "Yulai Federation Auth Templates v{}".format(__version__)
