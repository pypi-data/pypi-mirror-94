from munch import munchify
import logging


def expand_links(session, d):
    if "links" in d:
        for link in d["links"]:
            rel = link["rel"]
            href = link["href"]

            def call(address=href):

                resp = session.get(address)
                if resp.status_code != 200:
                    logging.error(f"calling {address} failed : {resp.status_code}")
                    return ""
                resp = resp.json()
                expand_links(session, resp)
                if type(resp) is list:
                    for r in resp:
                        expand_links(session, r)
                elif type(resp) is dict:
                    for k, v in resp.items():
                        if type(v) is dict and "links" in v:
                            expand_links(session, v)

                return munchify(resp)

            d[rel.replace("-", "_")] = call
        del d["links"]
