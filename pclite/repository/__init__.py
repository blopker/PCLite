from .. import logger
log = logger.get(__name__)
from .. import settings
from .. import http
from .. import async
import traceback

from .channel import Channel
from .repository import Repository
from .package import Package


__all__ = [Repository, Package, Channel]


def _make_repo(url, cache=False):
    log.debug('Getting repo at url %s', url)
    try:
        if cache is False:
            j = http.get_json(url).get('packages', [])
        else:
            j = cache
        print(j)
        if j:
            pkgs = [Package(x) for x in j]
            repo = Repository(*pkgs)
            log.debug('Processed repo at url %s', url)
            return repo
        else:
            log.debug('Processing failed for repo at url %s', url)
            log.debug(j)
            return False
    except:
        log.warning('Unable to fetch repository at %s', url)
        return False


def _get_channel(url):
    log.debug('Getting channel at %s', url)
    try:
        j = http.get_json(url)
        log.debug('Got channel at url %s', url)
        if j:
            channel = Channel(j)
            log.debug('Processed channel at url %s', url)
            return channel
        else:
            log.debug('Processing failed for channel at url %s', url)
            log.debug(j)
            return False
    except:
        log.warning('Unable to fetch channel at %s', url)
        return False


def update_repository():
    try:
        # Get all the channels
        channel_urls = settings.get('channels', [])
        channels = async.asyncMap(_get_channel, channel_urls)

        # Get all the repositories
        for channel in channels:
            if channel is False:
                continue
            cache = [channel.get_cache(url) for url in channel.urls()]
            repos = async.asyncMap(_make_repo, channel.urls(), cache)

        # Merge into one repo
        repo = Repository()
        for r in repos:
            repo.merge(r)

        if len(repo.packages) is 0:
            log.error('No packages found.')
            return False

        return repo
    except:
        log.error('Unable to get repository for unknown reason:')
        traceback.print_exc()
    return False
