# Import python libs
import asyncio
import json
import uuid
from typing import Any, Dict

__func_alias__ = {"compile_": "compile"}


async def create(
    hub,
    name,
    sls_sources,
    render,
    runtime,
    subs,
    cache_dir,
    test,
    acct_file,
    acct_key,
    acct_profile,
):
    """
    Create a new instance to execute against
    """
    if acct_file and acct_key:
        await hub.acct.init.unlock(acct_file, acct_key)

    hub.idem.RUNS[name] = {
        "sls_sources": sls_sources,
        "render": render,
        "runtime": runtime,
        "subs": subs,
        "cache_dir": cache_dir,
        "states": {},
        "test": test,
        "resolved": set(),
        "files": set(),
        "high": {},
        "post_low": [],
        "errors": [],
        "iorder": 100000,
        "sls_refs": {},
        "blocks": {},
        "running": {},
        "run_num": 1,
        "add_low": [],
        "acct_profile": acct_profile,
    }


async def apply(
    hub,
    name,
    sls_sources,
    render,
    runtime,
    subs,
    cache_dir,
    sls,
    test=False,
    acct_file=None,
    acct_key=None,
    acct_profile="default",
):
    """
    Run idem!
    """
    await hub.idem.state.create(
        name,
        sls_sources,
        render,
        runtime,
        subs,
        cache_dir,
        test,
        acct_file,
        acct_key,
        acct_profile,
    )
    # Get the sls file
    # render it
    # compile high data to "new" low data (bypass keyword issues)
    # Run the low data using act/idem
    await hub.idem.resolve.gather(name, *sls)
    if hub.idem.RUNS[name]["errors"]:
        return
    await hub.idem.state.compile(name)
    if hub.idem.RUNS[name]["errors"]:
        return
    return await hub.idem.run.init.start(name)


async def compile_(hub, name):
    """
    Compile the data defined in the given run name
    """
    for mod in hub.idem.compiler:
        if hasattr(mod, "stage"):
            ret = mod.stage(name)
            if asyncio.iscoroutine(ret):
                await ret


async def single(hub, _ref_: str, _test_: bool = None, *args, **kwargs):
    """
    Run a single state and return the raw result
    :param hub:
    :param _ref_: The state's reference on the hub
    :param _test_: Run the state in a low-consequence test-mode
    :param args: Args to be passed straight through to the state
    :param kwargs: Kwargs to be passed straight through to the state
    """
    if _test_ is None:
        _test_ = hub.OPT.idem.test

    acct_file = hub.OPT.acct.acct_file
    acct_key = hub.OPT.acct.acct_key
    acct_profile = hub.OPT.acct.get("acct_profile", "default")

    args = [a for a in args]

    if not _ref_.startswith("states."):
        _ref_ = f"states.{_ref_}"

    func = getattr(hub, _ref_)
    params = func.signature.parameters

    if "ctx" in params:
        ctx = await hub.idem.ex.ctx(_ref_, acct_file, acct_key, acct_profile)
        ctx.test = _test_
        args.insert(0, ctx)

    ret = func(*args, **kwargs)
    if asyncio.iscoroutine(ret):
        return await ret

    return ret


async def batch(
    hub, states: Dict[str, Dict[str, Any]], runtime: str = None, test: bool = None
):
    """
    Run multiple states defined in code
    :param hub:
    :param states:
    :param runtime: "serial" or "parallel"
    :param test: Set "test" to "True" in the implicit ctx parameter
    """
    name = "batch"
    sls_source = str(uuid.uuid4())

    if runtime is None:
        runtime = hub.OPT.idem.runtime
    if test is None:
        test = hub.OPT.idem.test

    acct_file = hub.OPT.acct.acct_file
    acct_key = hub.OPT.acct.acct_key
    acct_profile = hub.OPT.acct.get("acct_profile", "default")

    data = {sls_source: states}
    sls_sources = [f"json://{json.dumps(data)}"]
    sls = [sls_source]
    await hub.idem.state.apply(
        name=name,
        sls_sources=sls_sources,
        render=hub.OPT.idem.render,
        runtime=runtime,
        subs=["states"],
        cache_dir=hub.OPT.idem.cache_dir,
        sls=sls,
        test=test,
        acct_file=acct_file,
        acct_key=acct_key,
        acct_profile=acct_profile,
    )

    if hub.idem.RUNS[name]["errors"]:
        return hub.idem.RUNS[name]["errors"]

    return hub.idem.RUNS[name]["running"]
