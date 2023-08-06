from typing import Any, Dict, Iterable
from dict_tools.data import NamespaceDict
import asyncio

__func_alias__ = {"profiles_": "profiles"}


def __init__(hub):
    hub.acct.PROFILES = NamespaceDict()
    hub.acct.SUB_PROFILES = NamespaceDict()
    hub.acct.UNLOCKED = False
    hub.acct.DEFAULT = "default"
    hub.acct.BACKEND_KEY = "acct-backends"

    hub.pop.sub.add(dyne_name="crypto")
    hub.pop.sub.load_subdirs(hub.acct, recurse=True)


def cli(hub):
    hub.pop.sub.add(dyne_name="rend")
    hub.pop.config.load(["acct", "rend"], cli="acct")
    hub.pop.loop.create()

    if hub.SUBPARSER == "encrypt":
        if not hub.OPT.acct.acct_key:
            coro = hub.crypto.init.generate_key(hub.OPT.acct.crypto_plugin)
            acct_key = hub.pop.Loop.run_until_complete(coro)
            hub.log.info(
                f"New acct_key generated with '{hub.OPT.acct.crypto_plugin}' plugin"
            )
        else:
            acct_key = hub.OPT.acct.acct_key

        new_key = hub.pop.Loop.run_until_complete(
            hub.crypto.init.encrypt_file(
                crypto_plugin=hub.OPT.acct.crypto_plugin,
                acct_file=hub.OPT.acct.acct_file,
                acct_key=acct_key,
                output_file=hub.OPT.acct.output_file,
            )
        )
        hub.log.info(
            f"Encrypted {hub.OPT.acct.acct_file} with the {hub.OPT.acct.crypto_plugin} algorithm"
        )
        if not hub.OPT.acct.acct_key:
            # Print this to the terminal, and only this -- for easier scripting
            # Do not log it or put it in log files
            print(new_key)
    elif hub.SUBPARSER == "decrypt":
        ret = hub.pop.Loop.run_until_complete(
            hub.crypto.init.decrypt_file(
                crypto_plugin=hub.OPT.acct.crypto_plugin,
                acct_file=hub.OPT.acct.acct_file,
                acct_key=hub.OPT.acct.acct_key,
            )
        )
        out = hub.output[hub.OPT.rend.output].display(ret)
        print(out)


async def backends(hub, profiles: Dict[str, Any]):
    """
    Read the raw profiles and search for externally defined profiles.
    """
    # Allow custom specification of a backend key per acct_file
    backend_key = profiles.get("backend_key", hub.acct.BACKEND_KEY)

    ret = {}
    for backend, kwargs in profiles.get(backend_key, {}).items():
        if "profiles" in hub.acct.backend[backend].unlock.signature.parameters:
            backend_profiles = hub.acct.backend[backend].unlock(
                profiles=profiles, **kwargs
            )
        else:
            backend_profiles = hub.acct.backend[backend].unlock(**kwargs)

        if asyncio.iscoroutine(backend_profiles):
            backend_profiles = await backend_profiles

        # If an acct-backend specifies other backends, then recursively load them onto the same space
        if backend_key in backend_profiles:
            hub.pop.dicts.update(ret, await hub.acct.init.backends(backend_profiles))
        else:
            ret[backend] = backend_profiles

    return ret


async def profiles_(
    hub, acct_file: str, acct_key: str, crypto_plugin: str = "fernet"
) -> Dict[str, Any]:
    """
    Read profile information from a file and return the raw data
    """
    raw_profiles = await hub.crypto.init.decrypt_file(
        crypto_plugin=crypto_plugin,
        acct_file=acct_file,
        acct_key=acct_key,
    )
    backend_profiles = await hub.acct.init.backends(raw_profiles)
    hub.pop.dicts.update(raw_profiles, backend_profiles)
    return raw_profiles


async def process(hub, subs: Iterable[str], profiles: Dict[str, Any]):
    """
    Process the given profiles through acct plugins.
    Acct plugins turn static profile data into connections to a server etc...
    """
    processed = NamespaceDict()

    for sub in subs:
        if not hasattr(hub.acct, sub):
            hub.log.trace(f"{sub} does not extend acct")
            continue

        processed[sub] = {}
        for plug in hub.acct[sub]:
            if "profiles" in plug.gather.signature.parameters:
                ret = plug.gather(profiles)
            else:
                # It either doesn't need to know about existing profiles or will get them from hub.acct.PROFILES
                ret = plug.gather()
            if asyncio.iscoroutine(ret):
                ret = await ret
            processed[sub][plug.__name__] = ret
    return processed


async def unlock(hub, acct_file: str, acct_key: str, crypto_plugin: str = "fernet"):
    """
    Initialize the file read, then store the authentication data on the hub as hub.acct.PROFILES
    """
    if hub.acct.UNLOCKED:
        return
    raw_profiles = await hub.acct.init.profiles(acct_file, acct_key, crypto_plugin)
    hub.acct.BACKEND_KEY = raw_profiles.pop("backend_key", hub.acct.BACKEND_KEY)
    hub.acct.DEFAULT = raw_profiles.pop("default", hub.acct.DEFAULT)
    hub.pop.dicts.update(hub.acct.PROFILES, raw_profiles)
    hub.acct.UNLOCKED = True


async def single(
    hub,
    profile_name: str,
    subs: Iterable[str],
    sub_profiles: Dict[str, Dict[str, Any]],
    profiles: Dict[str, Dict[str, Any]],
):
    """
    Retrieve a specific named profile for the given subs, sub_profiles, and profiles
    """
    ret = NamespaceDict()

    for sub, plugin in sub_profiles.items():
        for sub_data in plugin.values():
            if not sub_data:
                continue
            if profile_name in sub_data:
                hub.pop.dicts.update(ret, sub_data[profile_name])
    for sub in subs:
        if sub in profiles:
            if profile_name in profiles[sub]:
                hub.pop.dicts.update(ret, hub.acct.PROFILES[sub][profile_name])

    return ret


async def gather(hub, subs: Iterable[str], profile: str) -> Dict[str, Dict[str, Any]]:
    """
    :param hub:
    :param subs: The subs to check for a profile
    :param profile: The name of the acct_profile to retrieve
    :return: The named profile
    """
    if not hub.acct.UNLOCKED:
        return {}

    unprocessed_subs = [sub for sub in subs if sub not in hub.acct.SUB_PROFILES]
    new_profiles = await hub.acct.init.process(unprocessed_subs, hub.acct.PROFILES)
    hub.pop.dicts.update(hub.acct.SUB_PROFILES, new_profiles)

    return await hub.acct.init.single(
        profile_name=profile,
        subs=subs,
        profiles=hub.acct.PROFILES,
        sub_profiles=hub.acct.SUB_PROFILES,
    )


async def close(hub):
    for sub, plugins in hub.acct.SUB_PROFILES.items():
        for plugin, profiles in plugins.items():
            if not hasattr(hub.acct[sub][plugin], "close"):
                continue

            ret = hub.acct[sub][plugin].close(profiles)
            if asyncio.iscoroutine(ret):
                await ret
