# coding=utf8
import logging

import requests

from xu.src.python.Request.Model import APIResponse, APIConfig, APIAnalysis


# GET
# POST
# PUT
# HEAD
# DELETE
# PATCH
# OPTIONS


def call(config: APIConfig) -> APIResponse:
    if config.protocol() == "POST":
        return run(requests.post, config)
    elif config.protocol() == "GET":
        return run(requests.get, config)
    elif config.protocol() == "PUT":
        return run(requests.put, config)
    elif config.protocol() == "HEAD":
        return run(requests.head, config)
    elif config.protocol() == "DELETE":
        return run(requests.delete, config)
    elif config.protocol() == "PATCH":
        return run(requests.patch, config)
    elif config.protocol() == "OPTIONS":
        return run(requests.options, config)


def run(func, config: APIConfig):
    url = config.parseLink().url() + config.api()
    param = config.param()
    body = config.body()
    header(config)
    try:
        if param != {} or param != "":
            if body != "" or body != {}:
                r = func(url=url, params=param, data=body, headers=config.header(), timeout=30)
            else:
                r = func(url=url, params=param, timeout=30)
        else:
            if body != "" or body != {}:
                r = func(url=url, data=body, headers=config.header(), timeout=30)
            else:
                r = func(url=url, timeout=30)
        data = response(r)
    except Exception as ex:
        logging.exception(ex)
        data = APIResponse()
        data.setStatus(400)
    return data


def header(config: APIConfig):
    if "Content-Type" not in config.header():
        config.header()["Content-Type"] = config.bodyType()


def response(r):
    # try:
    #     res = json.loads(r.content.decode("utf-8"))
    # except Exception as ex:
    #     res = r.content.decode("utf-8")
    # res = r.content.decode("utf-8")
    a = APIAnalysis()
    a.setStatusCode(r.status_code)
    a.setURL(r.url)
    a.setStatusName(print_response(r.status_code))
    a.setTotalTime(r.elapsed.total_seconds())
    a.setContentSize(len(r.content))

    data = APIResponse()
    data.setHeader(dict(r.headers))
    data.setContent(r.content)
    data.setStatus(r.status_code)
    data.setAnalysis(a)
    return data


def print_response(r):
    if r >= 500:
        return "Server error!!!"
    elif r >= 400:
        return "Client error!!!"
    elif r >= 300:
        return "Redirects!!!"
    elif r >= 200:
        return "Success!!!"
    elif r >= 100:
        return "Informational!!!"
    else:
        return "No Response"
