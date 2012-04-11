"""
shared stuff to keep logging consistent
"""
from constants import PAD


def PRINT_REQ(request):
    return "\n\n" + " -REQUEST- ".join([PAD, PAD]) + "\n\n" + str(request) + "\n\n"


def PRINT_RES(response):
    return "\n\n" + " -RESPONSE- ".join([PAD, PAD]) + "\n\n" + str(response) + "\n\n"
