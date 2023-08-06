__filename__ = "newsdaemon.py"
__author__ = "Bob Mottram"
__license__ = "AGPL3+"
__version__ = "1.2.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@freedombone.net"
__status__ = "Production"

# Example hashtag logic:
#
# if moderated and not #imcoxford then block
# if #pol and contains "westminster" then add #britpol
# if #unwantedtag then block

import os
import time
import datetime
import html
from shutil import rmtree
from subprocess import Popen
from collections import OrderedDict
from newswire import getDictFromNewswire
# from posts import sendSignedJson
from posts import createNewsPost
from posts import archivePostsForPerson
from content import validHashTag
from utils import removeHtml
from utils import getFullDomain
from utils import loadJson
from utils import saveJson
from utils import getStatusNumber
from utils import clearFromPostCaches
from utils import dangerousMarkup
from inbox import storeHashTags
from session import createSession


def _updateFeedsOutboxIndex(baseDir: str, domain: str, postId: str) -> None:
    """Updates the index used for imported RSS feeds
    """
    basePath = baseDir + '/accounts/news@' + domain
    indexFilename = basePath + '/outbox.index'

    if os.path.isfile(indexFilename):
        if postId not in open(indexFilename).read():
            try:
                with open(indexFilename, 'r+') as feedsFile:
                    content = feedsFile.read()
                    if postId + '\n' not in content:
                        feedsFile.seek(0, 0)
                        feedsFile.write(postId + '\n' + content)
                        print('DEBUG: feeds post added to index')
            except Exception as e:
                print('WARN: Failed to write entry to feeds posts index ' +
                      indexFilename + ' ' + str(e))
    else:
        feedsFile = open(indexFilename, 'w+')
        if feedsFile:
            feedsFile.write(postId + '\n')
            feedsFile.close()


def _saveArrivedTime(baseDir: str, postFilename: str, arrived: str) -> None:
    """Saves the time when an rss post arrived to a file
    """
    arrivedFile = open(postFilename + '.arrived', 'w+')
    if arrivedFile:
        arrivedFile.write(arrived)
        arrivedFile.close()


def _removeControlCharacters(content: str) -> str:
    """Remove escaped html
    """
    if '&' in content:
        return html.unescape(content)
    return content


def hashtagRuleResolve(tree: [], hashtags: [], moderated: bool,
                       content: str, url: str) -> bool:
    """Returns whether the tree for a hashtag rule evaluates to true or false
    """
    if not tree:
        return False

    if tree[0] == 'not':
        if len(tree) == 2:
            if isinstance(tree[1], str):
                return tree[1] not in hashtags
            elif isinstance(tree[1], list):
                return not hashtagRuleResolve(tree[1], hashtags, moderated,
                                              content, url)
    elif tree[0] == 'contains':
        if len(tree) == 2:
            matchStr = None
            if isinstance(tree[1], str):
                matchStr = tree[1]
            elif isinstance(tree[1], list):
                matchStr = tree[1][0]
            if matchStr:
                if matchStr.startswith('"') and matchStr.endswith('"'):
                    matchStr = matchStr[1:]
                    matchStr = matchStr[:len(matchStr) - 1]
                matchStrLower = matchStr.lower()
                contentWithoutTags = content.replace('#' + matchStrLower, '')
                return matchStrLower in contentWithoutTags
    elif tree[0] == 'from':
        if len(tree) == 2:
            matchStr = None
            if isinstance(tree[1], str):
                matchStr = tree[1]
            elif isinstance(tree[1], list):
                matchStr = tree[1][0]
            if matchStr:
                if matchStr.startswith('"') and matchStr.endswith('"'):
                    matchStr = matchStr[1:]
                    matchStr = matchStr[:len(matchStr) - 1]
                return matchStr.lower() in url
    elif tree[0] == 'and':
        if len(tree) >= 3:
            for argIndex in range(1, len(tree)):
                argValue = False
                if isinstance(tree[argIndex], str):
                    argValue = (tree[argIndex] in hashtags)
                elif isinstance(tree[argIndex], list):
                    argValue = hashtagRuleResolve(tree[argIndex],
                                                  hashtags, moderated,
                                                  content, url)
                if not argValue:
                    return False
            return True
    elif tree[0] == 'or':
        if len(tree) >= 3:
            for argIndex in range(1, len(tree)):
                argValue = False
                if isinstance(tree[argIndex], str):
                    argValue = (tree[argIndex] in hashtags)
                elif isinstance(tree[argIndex], list):
                    argValue = hashtagRuleResolve(tree[argIndex],
                                                  hashtags, moderated,
                                                  content, url)
                if argValue:
                    return True
            return False
    elif tree[0] == 'xor':
        if len(tree) >= 3:
            trueCtr = 0
            for argIndex in range(1, len(tree)):
                argValue = False
                if isinstance(tree[argIndex], str):
                    argValue = (tree[argIndex] in hashtags)
                elif isinstance(tree[argIndex], list):
                    argValue = hashtagRuleResolve(tree[argIndex],
                                                  hashtags, moderated,
                                                  content, url)
                if argValue:
                    trueCtr += 1
            if trueCtr == 1:
                return True
    elif tree[0].startswith('#') and len(tree) == 1:
        return tree[0] in hashtags
    elif tree[0].startswith('moderated'):
        return moderated
    elif tree[0].startswith('"') and tree[0].endswith('"'):
        return True

    return False


def hashtagRuleTree(operators: [],
                    conditionsStr: str,
                    tagsInConditions: [],
                    moderated: bool) -> []:
    """Walks the tree
    """
    if not operators and conditionsStr:
        conditionsStr = conditionsStr.strip()
        isStr = conditionsStr.startswith('"') and conditionsStr.endswith('"')
        if conditionsStr.startswith('#') or isStr or \
           conditionsStr in operators or \
           conditionsStr == 'moderated' or \
           conditionsStr == 'contains':
            if conditionsStr.startswith('#'):
                if conditionsStr not in tagsInConditions:
                    if ' ' not in conditionsStr or \
                       conditionsStr.startswith('"'):
                        tagsInConditions.append(conditionsStr)
            return [conditionsStr.strip()]
        else:
            return None
    if not operators or not conditionsStr:
        return None
    tree = None
    conditionsStr = conditionsStr.strip()
    isStr = conditionsStr.startswith('"') and conditionsStr.endswith('"')
    if conditionsStr.startswith('#') or isStr or \
       conditionsStr in operators or \
       conditionsStr == 'moderated' or \
       conditionsStr == 'contains':
        if conditionsStr.startswith('#'):
            if conditionsStr not in tagsInConditions:
                if ' ' not in conditionsStr or \
                   conditionsStr.startswith('"'):
                    tagsInConditions.append(conditionsStr)
        tree = [conditionsStr.strip()]
    ctr = 0
    while ctr < len(operators):
        op = operators[ctr]
        opMatch = ' ' + op + ' '
        if opMatch not in conditionsStr and \
           not conditionsStr.startswith(op + ' '):
            ctr += 1
            continue
        else:
            tree = [op]
            if opMatch in conditionsStr:
                sections = conditionsStr.split(opMatch)
            else:
                sections = conditionsStr.split(op + ' ', 1)
            for subConditionStr in sections:
                result = hashtagRuleTree(operators[ctr + 1:],
                                         subConditionStr,
                                         tagsInConditions, moderated)
                if result:
                    tree.append(result)
            break
    return tree


def _newswireHashtagProcessing(session, baseDir: str, postJsonObject: {},
                               hashtags: [], httpPrefix: str,
                               domain: str, port: int,
                               personCache: {},
                               cachedWebfingers: {},
                               federationList: [],
                               sendThreads: [], postLog: [],
                               moderated: bool, url: str) -> bool:
    """Applies hashtag rules to a news post.
    Returns true if the post should be saved to the news timeline
    of this instance
    """
    rulesFilename = baseDir + '/accounts/hashtagrules.txt'
    if not os.path.isfile(rulesFilename):
        return True
    rules = []
    with open(rulesFilename, "r") as f:
        rules = f.readlines()

    domainFull = getFullDomain(domain, port)

    # get the full text content of the post
    content = ''
    if postJsonObject['object'].get('content'):
        content += postJsonObject['object']['content']
    if postJsonObject['object'].get('summary'):
        content += ' ' + postJsonObject['object']['summary']
    content = content.lower()

    # actionOccurred = False
    operators = ('not', 'and', 'or', 'xor', 'from', 'contains')
    for ruleStr in rules:
        if not ruleStr:
            continue
        if not ruleStr.startswith('if '):
            continue
        if ' then ' not in ruleStr:
            continue
        conditionsStr = ruleStr.split('if ', 1)[1]
        conditionsStr = conditionsStr.split(' then ')[0]
        tagsInConditions = []
        tree = hashtagRuleTree(operators, conditionsStr,
                               tagsInConditions, moderated)
        if not hashtagRuleResolve(tree, hashtags, moderated, content, url):
            continue
        # the condition matches, so do something
        actionStr = ruleStr.split(' then ')[1].strip()

        # add a hashtag
        if actionStr.startswith('add '):
            addHashtag = actionStr.split('add ', 1)[1].strip()
            if addHashtag.startswith('#'):
                if addHashtag not in hashtags:
                    hashtags.append(addHashtag)
                htId = addHashtag.replace('#', '')
                if validHashTag(htId):
                    hashtagUrl = \
                        httpPrefix + "://" + domainFull + "/tags/" + htId
                    newTag = {
                        'href': hashtagUrl,
                        'name': addHashtag,
                        'type': 'Hashtag'
                    }
                    # does the tag already exist?
                    addTagObject = None
                    for t in postJsonObject['object']['tag']:
                        if t.get('type') and t.get('name'):
                            if t['type'] == 'Hashtag' and \
                               t['name'] == addHashtag:
                                addTagObject = t
                                break
                    # append the tag if it wasn't found
                    if not addTagObject:
                        postJsonObject['object']['tag'].append(newTag)
                    # add corresponding html to the post content
                    hashtagHtml = \
                        " <a href=\"" + hashtagUrl + \
                        "\" class=\"addedHashtag\" " + \
                        "rel=\"tag\">#<span>" + \
                        htId + "</span></a>"
                    content = postJsonObject['object']['content']
                    if hashtagHtml not in content:
                        if content.endswith('</p>'):
                            content = \
                                content[:len(content) - len('</p>')] + \
                                hashtagHtml + '</p>'
                        else:
                            content += hashtagHtml
                        postJsonObject['object']['content'] = content
                        storeHashTags(baseDir, 'news', postJsonObject)
                        # actionOccurred = True

        # remove a hashtag
        if actionStr.startswith('remove '):
            rmHashtag = actionStr.split('remove ', 1)[1].strip()
            if rmHashtag.startswith('#'):
                if rmHashtag in hashtags:
                    hashtags.remove(rmHashtag)
                htId = rmHashtag.replace('#', '')
                hashtagUrl = \
                    httpPrefix + "://" + domainFull + "/tags/" + htId
                # remove tag html from the post content
                hashtagHtml = \
                    "<a href=\"" + hashtagUrl + \
                    "\" class=\"addedHashtag\" " + \
                    "rel=\"tag\">#<span>" + \
                    htId + "</span></a>"
                content = postJsonObject['object']['content']
                if hashtagHtml in content:
                    content = \
                        content.replace(hashtagHtml, '').replace('  ', ' ')
                    postJsonObject['object']['content'] = content
                rmTagObject = None
                for t in postJsonObject['object']['tag']:
                    if t.get('type') and t.get('name'):
                        if t['type'] == 'Hashtag' and \
                           t['name'] == rmHashtag:
                            rmTagObject = t
                            break
                if rmTagObject:
                    postJsonObject['object']['tag'].remove(rmTagObject)
                    # actionOccurred = True

        # Block this item
        if actionStr.startswith('block') or actionStr.startswith('drop'):
            return False
    return True


def _createNewsMirror(baseDir: str, domain: str,
                      postIdNumber: str, url: str,
                      maxMirroredArticles: int) -> bool:
    """Creates a local mirror of a news article
    """
    if '|' in url or '>' in url:
        return True

    mirrorDir = baseDir + '/accounts/newsmirror'
    if not os.path.isdir(mirrorDir):
        os.mkdir(mirrorDir)

    # count the directories
    noOfDirs = 0
    for subdir, dirs, files in os.walk(mirrorDir):
        noOfDirs = len(dirs)

    mirrorIndexFilename = baseDir + '/accounts/newsmirror.txt'

    if maxMirroredArticles > 0 and noOfDirs > maxMirroredArticles:
        if not os.path.isfile(mirrorIndexFilename):
            # no index for mirrors found
            return True
        removals = []
        with open(mirrorIndexFilename, 'r') as indexFile:
            # remove the oldest directories
            ctr = 0
            while noOfDirs > maxMirroredArticles:
                ctr += 1
                if ctr > 5000:
                    # escape valve
                    break

                postId = indexFile.readline()
                if not postId:
                    continue
                postId = postId.strip()
                mirrorArticleDir = mirrorDir + '/' + postId
                if os.path.isdir(mirrorArticleDir):
                    rmtree(mirrorArticleDir)
                    removals.append(postId)
                    noOfDirs -= 1

        # remove the corresponding index entries
        if removals:
            indexContent = ''
            with open(mirrorIndexFilename, 'r') as indexFile:
                indexContent = indexFile.read()
                for removePostId in removals:
                    indexContent = \
                        indexContent.replace(removePostId + '\n', '')
            with open(mirrorIndexFilename, "w+") as indexFile:
                indexFile.write(indexContent)

    mirrorArticleDir = mirrorDir + '/' + postIdNumber
    if os.path.isdir(mirrorArticleDir):
        # already mirrored
        return True

    # for onion instances mirror via tor
    prefixStr = ''
    if domain.endswith('.onion'):
        prefixStr = '/usr/bin/torsocks '

    # download the files
    commandStr = \
        prefixStr + '/usr/bin/wget -mkEpnp -e robots=off ' + url + \
        ' -P ' + mirrorArticleDir
    p = Popen(commandStr, shell=True)
    os.waitpid(p.pid, 0)

    if not os.path.isdir(mirrorArticleDir):
        print('WARN: failed to mirror ' + url)
        return True

    # append the post Id number to the index file
    if os.path.isfile(mirrorIndexFilename):
        indexFile = open(mirrorIndexFilename, "a+")
        if indexFile:
            indexFile.write(postIdNumber + '\n')
            indexFile.close()
    else:
        indexFile = open(mirrorIndexFilename, "w+")
        if indexFile:
            indexFile.write(postIdNumber + '\n')
            indexFile.close()

    return True


def _convertRSStoActivityPub(baseDir: str, httpPrefix: str,
                             domain: str, port: int,
                             newswire: {},
                             translate: {},
                             recentPostsCache: {}, maxRecentPosts: int,
                             session, cachedWebfingers: {},
                             personCache: {},
                             federationList: [],
                             sendThreads: [], postLog: [],
                             maxMirroredArticles: int,
                             allowLocalNetworkAccess: bool) -> None:
    """Converts rss items in a newswire into posts
    """
    if not newswire:
        return

    basePath = baseDir + '/accounts/news@' + domain + '/outbox'
    if not os.path.isdir(basePath):
        os.mkdir(basePath)

    # oldest items first
    newswireReverse = \
        OrderedDict(sorted(newswire.items(), reverse=False))

    for dateStr, item in newswireReverse.items():
        originalDateStr = dateStr
        # convert the date to the format used by ActivityPub
        if '+00:00' in dateStr:
            dateStr = dateStr.replace(' ', 'T')
            dateStr = dateStr.replace('+00:00', 'Z')
        else:
            dateStrWithOffset = \
                datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S%z")
            dateStr = dateStrWithOffset.strftime("%Y-%m-%dT%H:%M:%SZ")

        statusNumber, published = getStatusNumber(dateStr)
        newPostId = \
            httpPrefix + '://' + domain + \
            '/users/news/statuses/' + statusNumber

        # file where the post is stored
        filename = basePath + '/' + newPostId.replace('/', '#') + '.json'
        if os.path.isfile(filename):
            # don't create the post if it already exists
            # set the url
            # newswire[originalDateStr][1] = \
            #     '/users/news/statuses/' + statusNumber
            # set the filename
            newswire[originalDateStr][3] = filename
            continue

        rssTitle = _removeControlCharacters(item[0])
        url = item[1]
        if dangerousMarkup(url, allowLocalNetworkAccess) or \
           dangerousMarkup(rssTitle, allowLocalNetworkAccess):
            continue
        rssDescription = ''

        # get the rss description if it exists
        rssDescription = '<p>' + removeHtml(item[4]) + '<p>'

        mirrored = item[7]
        postUrl = url
        if mirrored and '://' in url:
            postUrl = '/newsmirror/' + statusNumber + '/' + \
                url.split('://')[1]
            if postUrl.endswith('/'):
                postUrl += 'index.html'
            else:
                postUrl += '/index.html'

        # add the off-site link to the description
        rssDescription += \
            '<br><a href="' + postUrl + '">' + \
            translate['Read more...'] + '</a>'

        followersOnly = False
        # NOTE: the id when the post is created will not be
        # consistent (it's based on the current time, not the
        # published time), so we change that later
        blog = createNewsPost(baseDir,
                              domain, port, httpPrefix,
                              rssDescription,
                              followersOnly, False,
                              None, None, None,
                              rssTitle)
        if not blog:
            continue

        if mirrored:
            if not _createNewsMirror(baseDir, domain, statusNumber,
                                     url, maxMirroredArticles):
                continue

        idStr = \
            httpPrefix + '://' + domain + '/users/news' + \
            '/statuses/' + statusNumber + '/replies'
        blog['news'] = True

        # note the time of arrival
        currTime = datetime.datetime.utcnow()
        blog['object']['arrived'] = currTime.strftime("%Y-%m-%dT%H:%M:%SZ")

        # change the id, based upon the published time
        blog['object']['replies']['id'] = idStr
        blog['object']['replies']['first']['partOf'] = idStr

        blog['id'] = newPostId + '/activity'
        blog['object']['id'] = newPostId
        blog['object']['atomUri'] = newPostId
        blog['object']['url'] = \
            httpPrefix + '://' + domain + '/@news/' + statusNumber
        blog['object']['published'] = dateStr

        blog['object']['content'] = rssDescription
        blog['object']['contentMap']['en'] = rssDescription

        domainFull = getFullDomain(domain, port)

        hashtags = item[6]

        postId = newPostId.replace('/', '#')

        moderated = item[5]

        savePost = _newswireHashtagProcessing(session, baseDir, blog, hashtags,
                                              httpPrefix, domain, port,
                                              personCache, cachedWebfingers,
                                              federationList,
                                              sendThreads, postLog,
                                              moderated, url)

        # save the post and update the index
        if savePost:
            # ensure that all hashtags are stored in the json
            # and appended to the content
            blog['object']['tag'] = []
            for tagName in hashtags:
                htId = tagName.replace('#', '')
                hashtagUrl = \
                    httpPrefix + "://" + domainFull + "/tags/" + htId
                newTag = {
                    'href': hashtagUrl,
                    'name': tagName,
                    'type': 'Hashtag'
                }
                blog['object']['tag'].append(newTag)
                hashtagHtml = \
                    " <a href=\"" + hashtagUrl + \
                    "\" class=\"addedHashtag\" " + \
                    "rel=\"tag\">#<span>" + \
                    htId + "</span></a>"
                content = blog['object']['content']
                if hashtagHtml not in content:
                    if content.endswith('</p>'):
                        content = \
                            content[:len(content) - len('</p>')] + \
                            hashtagHtml + '</p>'
                    else:
                        content += hashtagHtml
                    blog['object']['content'] = content

            # update the newswire tags if new ones have been found by
            # _newswireHashtagProcessing
            for tag in hashtags:
                if tag not in newswire[originalDateStr][6]:
                    newswire[originalDateStr][6].append(tag)

            storeHashTags(baseDir, 'news', blog)

            clearFromPostCaches(baseDir, recentPostsCache, postId)
            if saveJson(blog, filename):
                _updateFeedsOutboxIndex(baseDir, domain, postId + '.json')

                # Save a file containing the time when the post arrived
                # this can then later be used to construct the news timeline
                # excluding items during the voting period
                if moderated:
                    _saveArrivedTime(baseDir, filename,
                                     blog['object']['arrived'])
                else:
                    if os.path.isfile(filename + '.arrived'):
                        os.remove(filename + '.arrived')

                # setting the url here links to the activitypub object
                # stored locally
                # newswire[originalDateStr][1] = \
                #     '/users/news/statuses/' + statusNumber

                # set the filename
                newswire[originalDateStr][3] = filename


def _mergeWithPreviousNewswire(oldNewswire: {}, newNewswire: {}) -> None:
    """Preserve any votes or generated activitypub post filename
    as rss feeds are updated
    """
    if not oldNewswire:
        return

    for published, fields in oldNewswire.items():
        if not newNewswire.get(published):
            continue
        for i in range(1, 5):
            newNewswire[published][i] = fields[i]


def runNewswireDaemon(baseDir: str, httpd,
                      httpPrefix: str, domain: str, port: int,
                      translate: {}) -> None:
    """Periodically updates RSS feeds
    """
    newswireStateFilename = baseDir + '/accounts/.newswirestate.json'

    # initial sleep to allow the system to start up
    time.sleep(50)
    while True:
        # has the session been created yet?
        if not httpd.session:
            print('Newswire daemon waiting for session')
            httpd.session = createSession(httpd.proxyType)
            if not httpd.session:
                print('Newswire daemon has no session')
                time.sleep(60)
                continue
            else:
                print('Newswire daemon session established')

        # try to update the feeds
        newNewswire = \
            getDictFromNewswire(httpd.session, baseDir, domain,
                                httpd.maxNewswirePostsPerSource,
                                httpd.maxNewswireFeedSizeKb,
                                httpd.maxTags,
                                httpd.maxFeedItemSizeKb,
                                httpd.maxNewswirePosts,
                                httpd.maxCategoriesFeedItemSizeKb)

        if not httpd.newswire:
            if os.path.isfile(newswireStateFilename):
                httpd.newswire = loadJson(newswireStateFilename)

        _mergeWithPreviousNewswire(httpd.newswire, newNewswire)

        httpd.newswire = newNewswire
        if newNewswire:
            saveJson(httpd.newswire, newswireStateFilename)
            print('Newswire updated')

        _convertRSStoActivityPub(baseDir,
                                 httpPrefix, domain, port,
                                 newNewswire, translate,
                                 httpd.recentPostsCache,
                                 httpd.maxRecentPosts,
                                 httpd.session,
                                 httpd.cachedWebfingers,
                                 httpd.personCache,
                                 httpd.federationList,
                                 httpd.sendThreads,
                                 httpd.postLog,
                                 httpd.maxMirroredArticles,
                                 httpd.allowLocalNetworkAccess)
        print('Newswire feed converted to ActivityPub')

        if httpd.maxNewsPosts > 0:
            archiveDir = baseDir + '/archive'
            archiveSubdir = \
                archiveDir + '/accounts/news@' + domain + '/outbox'
            archivePostsForPerson(httpPrefix, 'news',
                                  domain, baseDir, 'outbox',
                                  archiveSubdir,
                                  httpd.recentPostsCache,
                                  httpd.maxNewsPosts)

        # wait a while before the next feeds update
        time.sleep(1200)


def runNewswireWatchdog(projectVersion: str, httpd) -> None:
    """This tries to keep the newswire update thread running even if it dies
    """
    print('Starting newswire watchdog')
    newswireOriginal = \
        httpd.thrPostSchedule.clone(runNewswireDaemon)
    httpd.thrNewswireDaemon.start()
    while True:
        time.sleep(50)
        if not httpd.thrNewswireDaemon.is_alive():
            httpd.thrNewswireDaemon.kill()
            httpd.thrNewswireDaemon = \
                newswireOriginal.clone(runNewswireDaemon)
            httpd.thrNewswireDaemon.start()
            print('Restarting newswire daemon...')
