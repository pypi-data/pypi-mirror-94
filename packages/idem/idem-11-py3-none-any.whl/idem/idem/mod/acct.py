# Import python libs
import asyncio


async def modify(hub, name, chunk):
    """
    Check the state containing the target func and call the mod_creds
    function if present. Therefore gathering the list of creds systems
    to use
    """
    run_name = chunk["ctx"]["run_name"]
    state = chunk["state"].split(".")[0]
    subs = []
    if hasattr(hub, f"states.{state}.ACCT"):
        subs = getattr(hub, f"states.{state}.ACCT")
    elif hasattr(hub, f"{state}.ACCT"):
        subs = getattr(hub, f"{state}.ACCT")
    elif hasattr(hub, f"exec.{state}.ACCT"):
        subs = getattr(hub, f"exec.{state}.ACCT")
    elif hasattr(hub, f"tool.{state}.ACCT"):
        subs = getattr(hub, f"tool.{state}.ACCT")
    hub.log.debug(f"Loaded acct from subs: {subs}")
    profile = chunk.pop("acct_profile", hub.idem.RUNS[run_name]["acct_profile"])
    hub.log.debug(f"Loaded profile: {profile}")
    chunk["ctx"]["acct"] = await hub.acct.init.gather(subs, profile)
    return chunk
