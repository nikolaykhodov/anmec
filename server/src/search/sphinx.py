# -*- coding: utf8 -*-

from django.conf import settings
import sphinxapi

def search_for(query, index):
    """

    Returns ID of objects

    """

    client = sphinxapi.SphinxClient()
    client.SetServer(settings.SPHINX_SERVER, settings.SPHINX_PORT)
    client.SetMatchMode(sphinxapi.SPH_MATCH_ALL)
    client.SetSortMode(sphinxapi.SPH_SORT_RELEVANCE)
    client.SetLimits(0, settings.SPHINX_MAXMATCHES, maxmatches=settings.SPHINX_MAXMATCHES)

    result = client.Query(query, index)

    if result is None:
        raise Exception, client.GetLastError()

    if result.has_key('matches') is False:
        return []

    return [match['id'] for match in result['matches']]
