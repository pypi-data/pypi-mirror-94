def stage(hub, name):
    high, errors = hub.idem.ccomps.verify.high(hub.idem.RUNS[name]["high"])
    hub.idem.RUNS[name]["high"] = high
    hub.idem.RUNS[name]["errors"] = errors
