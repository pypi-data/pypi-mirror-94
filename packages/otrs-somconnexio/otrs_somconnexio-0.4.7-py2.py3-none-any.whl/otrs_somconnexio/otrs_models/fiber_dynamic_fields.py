# coding: utf-8
from otrs_somconnexio.otrs_models.internet_dynamic_fields import InternetDynamicFields


class FiberDynamicFields(InternetDynamicFields):

    def _build_specific_broadband_service_dynamic_fields(self):
        """ Return list of OTRS DynamicFields to create a OTRS Process Ticket from service data and customer data.
        Return only the specifics fields of Fiber Ticket. """
        return []
