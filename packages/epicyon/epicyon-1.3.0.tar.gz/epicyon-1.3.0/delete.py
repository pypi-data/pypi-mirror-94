__filename__ = "delete.py"
__author__ = "Bob Mottram"
__license__ = "AGPL3+"
__version__ = "1.2.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@freedombone.net"
__status__ = "Production"

import os
from datetime import datetime
from utils import hasUsersPath
from utils import getFullDomain
from utils import removeIdEnding
from utils import getNicknameFromActor
from utils import getDomainFromActor
from utils import locatePost
from utils import deletePost
from utils import removeModerationPostFromIndex
from session import postJson
from webfinger import webfingerHandle
from auth import createBasicAuthHeader
from posts import getPersonBox


def sendDeleteViaServer(baseDir: str, session,
                        fromNickname: str, password: str,
                        fromDomain: str, fromPort: int,
                        httpPrefix: str, deleteObjectUrl: str,
                        cachedWebfingers: {}, personCache: {},
                        debug: bool, projectVersion: str) -> {}:
    """Creates a delete request message via c2s
    """
    if not session:
        print('WARN: No session for sendDeleteViaServer')
        return 6

    fromDomainFull = getFullDomain(fromDomain, fromPort)

    actor = httpPrefix + '://' + fromDomainFull + \
        '/users/' + fromNickname
    toUrl = 'https://www.w3.org/ns/activitystreams#Public'
    ccUrl = actor + '/followers'

    newDeleteJson = {
        "@context": "https://www.w3.org/ns/activitystreams",
        'actor': actor,
        'cc': [ccUrl],
        'object': deleteObjectUrl,
        'to': [toUrl],
        'type': 'Delete'
    }

    handle = httpPrefix + '://' + fromDomainFull + '/@' + fromNickname

    # lookup the inbox for the To handle
    wfRequest = \
        webfingerHandle(session, handle, httpPrefix, cachedWebfingers,
                        fromDomain, projectVersion)
    if not wfRequest:
        if debug:
            print('DEBUG: announce webfinger failed for ' + handle)
        return 1
    if not isinstance(wfRequest, dict):
        print('WARN: Webfinger for ' + handle + ' did not return a dict. ' +
              str(wfRequest))
        return 1

    postToBox = 'outbox'

    # get the actor inbox for the To handle
    (inboxUrl, pubKeyId, pubKey,
     fromPersonId, sharedInbox, avatarUrl,
     displayName) = getPersonBox(baseDir, session, wfRequest, personCache,
                                 projectVersion, httpPrefix, fromNickname,
                                 fromDomain, postToBox, 53036)

    if not inboxUrl:
        if debug:
            print('DEBUG: No ' + postToBox + ' was found for ' + handle)
        return 3
    if not fromPersonId:
        if debug:
            print('DEBUG: No actor was found for ' + handle)
        return 4

    authHeader = createBasicAuthHeader(fromNickname, password)

    headers = {
        'host': fromDomain,
        'Content-type': 'application/json',
        'Authorization': authHeader
    }
    postResult = \
        postJson(session, newDeleteJson, [], inboxUrl, headers)
    if not postResult:
        if debug:
            print('DEBUG: POST announce failed for c2s to ' + inboxUrl)
        return 5

    if debug:
        print('DEBUG: c2s POST delete request success')

    return newDeleteJson


def outboxDelete(baseDir: str, httpPrefix: str,
                 nickname: str, domain: str,
                 messageJson: {}, debug: bool,
                 allowDeletion: bool,
                 recentPostsCache: {}) -> None:
    """ When a delete request is received by the outbox from c2s
    """
    if not messageJson.get('type'):
        if debug:
            print('DEBUG: delete - no type')
        return
    if not messageJson['type'] == 'Delete':
        if debug:
            print('DEBUG: not a delete')
        return
    if not messageJson.get('object'):
        if debug:
            print('DEBUG: no object in delete')
        return
    if not isinstance(messageJson['object'], str):
        if debug:
            print('DEBUG: delete object is not string')
        return
    if debug:
        print('DEBUG: c2s delete request arrived in outbox')
    deletePrefix = httpPrefix + '://' + domain
    if (not allowDeletion and
        (not messageJson['object'].startswith(deletePrefix) or
         not messageJson['actor'].startswith(deletePrefix))):
        if debug:
            print('DEBUG: delete not permitted from other instances')
        return
    messageId = removeIdEnding(messageJson['object'])
    if '/statuses/' not in messageId:
        if debug:
            print('DEBUG: c2s delete object is not a status')
        return
    if not hasUsersPath(messageId):
        if debug:
            print('DEBUG: c2s delete object has no nickname')
        return
    deleteNickname = getNicknameFromActor(messageId)
    if deleteNickname != nickname:
        if debug:
            print("DEBUG: you can't delete a post which " +
                  "wasn't created by you (nickname does not match)")
        return
    deleteDomain, deletePort = getDomainFromActor(messageId)
    if ':' in domain:
        domain = domain.split(':')[0]
    if deleteDomain != domain:
        if debug:
            print("DEBUG: you can't delete a post which " +
                  "wasn't created by you (domain does not match)")
        return
    removeModerationPostFromIndex(baseDir, messageId, debug)
    postFilename = locatePost(baseDir, deleteNickname, deleteDomain,
                              messageId)
    if not postFilename:
        if debug:
            print('DEBUG: c2s delete post not found in inbox or outbox')
            print(messageId)
        return True
    deletePost(baseDir, httpPrefix, deleteNickname, deleteDomain,
               postFilename, debug, recentPostsCache)
    if debug:
        print('DEBUG: post deleted via c2s - ' + postFilename)


def removeOldHashtags(baseDir: str, maxMonths: int) -> str:
    """Remove old hashtags
    """
    if maxMonths > 11:
        maxMonths = 11
    maxDaysSinceEpoch = \
        (datetime.utcnow() - datetime(1970, 1 + maxMonths, 1)).days
    removeHashtags = []

    for subdir, dirs, files in os.walk(baseDir + '/tags'):
        for f in files:
            tagsFilename = os.path.join(baseDir + '/tags', f)
            if not os.path.isfile(tagsFilename):
                continue
            # get last modified datetime
            modTimesinceEpoc = os.path.getmtime(tagsFilename)
            lastModifiedDate = datetime.fromtimestamp(modTimesinceEpoc)
            fileDaysSinceEpoch = (lastModifiedDate - datetime(1970, 1, 1)).days

            # check of the file is too old
            if fileDaysSinceEpoch < maxDaysSinceEpoch:
                removeHashtags.append(tagsFilename)
        break

    for removeFilename in removeHashtags:
        try:
            os.remove(removeFilename)
        except BaseException:
            pass
