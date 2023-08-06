import time
import numpy as np
from scipy.stats import norm
from django.conf import settings
from django.http import HttpResponseForbidden   
class LatencyMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
     
        if 'DEBUG_ONLY' in settings.NETWORK_CONDITIONS.keys():
            self.debug = settings.NETWORK_CONDITIONS["DEBUG_ONLY"]
        else:
            self.debug = True
        self.latency = settings.NETWORK_CONDITIONS["LATENCY"] 
        self.jitter = settings.NETWORK_CONDITIONS["JITTER"] 
        self.timeout_pct = settings.NETWORK_CONDITIONS["TIMEOUT_PCT"]
        self.kb_per_second = settings.NETWORK_CONDITIONS["KB_PER_SECOND"]
        self.delay = np.random.normal(self.latency, self.jitter)
        self.print_logs = settings.NETWORK_CONDITIONS["PRINT_LOGS"]

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        if self.debug:
            if self.delay < 0:
                self.delay = 0
            threshold = norm.ppf((1 - self.timeout_pct/100), self.latency, self.jitter)
            if self.delay < threshold:                
                response_datasaze = len(response.content)
                transmit_delay = response_datasaze / self.kb_per_second
                final_delay = self.delay + transmit_delay
                if self.print_logs:
                    print("threshold", threshold)
                    print("random delay", self.delay)
                    print("respond data size", response_datasaze)
                    print("transmission delay", transmit_delay)
                    print("finally", final_delay)
                    print("delaying...")
                time.sleep(final_delay)
            else:
                return HttpResponseForbidden()
        return response