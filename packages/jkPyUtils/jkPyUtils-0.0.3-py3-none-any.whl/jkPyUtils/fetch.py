import requests
import time

import mimetypes

from jkPyUtils.icache import cache


SLEEP_SECONDS = 5

timer_pool = {}


# @API
def get_url_text(url, enable_cache=True):
    if enable_cache:
        rsp = _get_url_with_cache(url)
    else:
        rsp = _get_url(url)

    if not rsp:
        return

    text = rsp.text.encode(rsp.encoding).decode('utf8')
    return text


# @API
def get_url_binary(url):
    rsp = _get_url(url)
    if not rsp:
        return None, None

    binary = rsp.content
    # ext is '' if Content-Type unknown or not exist
    ext = mimetypes.guess_extension(rsp.headers.get('Content-Type', ''))
    return binary, ext


def _get_url(url, timeout=15):
    # print(url)
    timer_key = 'last_request'

    tic = time.time()
    if timer_key in timer_pool:
        toc = timer_pool[timer_key] + SLEEP_SECONDS
        gap = toc - tic
        if gap > 0:
            # print('sleeping %s seconds' % gap)
            time.sleep(gap)

    timer_pool[timer_key] = time.time()

    try:
        rsp = requests.get(url, timeout=timeout)
    except requests.exceptions.ReadTimeout:
        print('!!! timeout. url: %s' % url)
        return
    except requests.exceptions.ConnectionError as e:
        print('!!! ConnectionError. url: %s' % url)
        return
        # print('!!! connect error: %s. sleep %ss and retry' % (e, SLEEP_SECONDS))
        # time.sleep(SLEEP_SECONDS)
        # rsp = requests.get(url, timeout=timeout)

    # print(rsp.url)
    if rsp.status_code != 200:
        return

    return rsp


@cache
def _get_url_with_cache(*args, **kwargs):
    return _get_url(*args, **kwargs)
