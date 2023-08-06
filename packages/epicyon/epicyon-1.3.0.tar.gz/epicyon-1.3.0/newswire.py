__filename__ = "newswire.py"
__author__ = "Bob Mottram"
__license__ = "AGPL3+"
__version__ = "1.2.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@freedombone.net"
__status__ = "Production"

import os
import requests
from socket import error as SocketError
import errno
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from collections import OrderedDict
from utils import validPostDate
from categories import setHashtagCategory
from utils import firstParagraphFromString
from utils import isPublicPost
from utils import locatePost
from utils import loadJson
from utils import saveJson
from utils import isSuspended
from utils import containsInvalidChars
from utils import removeHtml
from blocking import isBlockedDomain
from blocking import isBlockedHashtag
from filters import isFiltered


def _removeCDATA(text: str) -> str:
    """Removes any CDATA from the given text
    """
    if 'CDATA[' in text:
        text = text.split('CDATA[')[1]
        if ']' in text:
            text = text.split(']')[0]
    return text


def rss2Header(httpPrefix: str,
               nickname: str, domainFull: str,
               title: str, translate: {}) -> str:
    """Header for an RSS 2.0 feed
    """
    rssStr = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"
    rssStr += "<rss version=\"2.0\">"
    rssStr += '<channel>'

    if title.startswith('News'):
        rssStr += '    <title>Newswire</title>'
        rssStr += '    <link>' + httpPrefix + '://' + domainFull + \
            '/newswire.xml' + '</link>'
    elif title.startswith('Site'):
        rssStr += '    <title>' + domainFull + '</title>'
        rssStr += '    <link>' + httpPrefix + '://' + domainFull + \
            '/blog/rss.xml' + '</link>'
    else:
        rssStr += '    <title>' + translate[title] + '</title>'
        rssStr += '    <link>' + httpPrefix + '://' + domainFull + \
            '/users/' + nickname + '/rss.xml' + '</link>'
    return rssStr


def rss2Footer() -> str:
    """Footer for an RSS 2.0 feed
    """
    rssStr = '</channel>'
    rssStr += '</rss>'
    return rssStr


def getNewswireTags(text: str, maxTags: int) -> []:
    """Returns a list of hashtags found in the given text
    """
    if '#' not in text:
        return []
    if ' ' not in text:
        return []
    textSimplified = \
        text.replace(',', ' ').replace(';', ' ').replace('- ', ' ')
    textSimplified = textSimplified.replace('. ', ' ').strip()
    if textSimplified.endswith('.'):
        textSimplified = textSimplified[:len(textSimplified)-1]
    words = textSimplified.split(' ')
    tags = []
    for wrd in words:
        if wrd.startswith('#'):
            if len(wrd) > 1:
                if wrd not in tags:
                    tags.append(wrd)
                    if len(tags) >= maxTags:
                        break
    return tags


def _addNewswireDictEntry(baseDir: str, domain: str,
                          newswire: {}, dateStr: str,
                          title: str, link: str,
                          votesStatus: str, postFilename: str,
                          description: str, moderated: bool,
                          mirrored: bool,
                          tags=[], maxTags=32) -> None:
    """Update the newswire dictionary
    """
    # remove any markup
    title = removeHtml(title)
    description = removeHtml(description)

    allText = title + ' ' + description

    # check that none of the text is filtered against
    if isFiltered(baseDir, None, None, allText):
        return

    if tags is None:
        tags = []

    # extract hashtags from the text of the feed post
    postTags = getNewswireTags(allText, maxTags)

    # combine the tags into a single list
    for tag in tags:
        if tag not in postTags:
            if len(postTags) < maxTags:
                postTags.append(tag)

    # check that no tags are blocked
    for tag in postTags:
        if isBlockedHashtag(baseDir, tag):
            return

    newswire[dateStr] = [
        title,
        link,
        votesStatus,
        postFilename,
        description,
        moderated,
        postTags,
        mirrored
    ]


def _validFeedDate(pubDate: str) -> bool:
    # convert from YY-MM-DD HH:MM:SS+00:00 to
    # YY-MM-DDTHH:MM:SSZ
    postDate = pubDate.replace(' ', 'T').replace('+00:00', 'Z')
    return validPostDate(postDate, 30)


def parseFeedDate(pubDate: str) -> str:
    """Returns a UTC date string based on the given date string
    This tries a number of formats to see which work
    """
    formats = ("%a, %d %b %Y %H:%M:%S %z",
               "%a, %d %b %Y %H:%M:%S EST",
               "%a, %d %b %Y %H:%M:%S UT",
               "%Y-%m-%dT%H:%M:%SZ",
               "%Y-%m-%dT%H:%M:%S%z")

    publishedDate = None
    for dateFormat in formats:
        if ',' in pubDate and ',' not in dateFormat:
            continue
        if ',' not in pubDate and ',' in dateFormat:
            continue
        if 'Z' in pubDate and 'Z' not in dateFormat:
            continue
        if 'Z' not in pubDate and 'Z' in dateFormat:
            continue
        if 'EST' not in pubDate and 'EST' in dateFormat:
            continue
        if 'EST' in pubDate and 'EST' not in dateFormat:
            continue
        if 'UT' not in pubDate and 'UT' in dateFormat:
            continue
        if 'UT' in pubDate and 'UT' not in dateFormat:
            continue

        try:
            publishedDate = \
                datetime.strptime(pubDate, dateFormat)
        except BaseException:
            print('WARN: unrecognized date format: ' +
                  pubDate + ' ' + dateFormat)
            continue

        if publishedDate:
            if pubDate.endswith(' EST'):
                hoursAdded = timedelta(hours=5)
                publishedDate = publishedDate + hoursAdded
            break

    pubDateStr = None
    if publishedDate:
        offset = publishedDate.utcoffset()
        if offset:
            publishedDate = publishedDate - offset
        # convert local date to UTC
        publishedDate = publishedDate.replace(tzinfo=timezone.utc)
        pubDateStr = str(publishedDate)
        if not pubDateStr.endswith('+00:00'):
            pubDateStr += '+00:00'

    return pubDateStr


def loadHashtagCategories(baseDir: str, language: str) -> None:
    """Loads an rss file containing hashtag categories
    """
    hashtagCategoriesFilename = baseDir + '/categories.xml'
    if not os.path.isfile(hashtagCategoriesFilename):
        hashtagCategoriesFilename = \
            baseDir + '/defaultcategories/' + language + '.xml'
        if not os.path.isfile(hashtagCategoriesFilename):
            return

    with open(hashtagCategoriesFilename, 'r') as fp:
        xmlStr = fp.read()
        _xml2StrToHashtagCategories(baseDir, xmlStr, 1024, True)


def _xml2StrToHashtagCategories(baseDir: str, xmlStr: str,
                                maxCategoriesFeedItemSizeKb: int,
                                force=False) -> None:
    """Updates hashtag categories based upon an rss feed
    """
    rssItems = xmlStr.split('<item>')
    maxBytes = maxCategoriesFeedItemSizeKb * 1024
    for rssItem in rssItems:
        if not rssItem:
            continue
        if len(rssItem) > maxBytes:
            print('WARN: rss categories feed item is too big')
            continue
        if '<title>' not in rssItem:
            continue
        if '</title>' not in rssItem:
            continue
        if '<description>' not in rssItem:
            continue
        if '</description>' not in rssItem:
            continue
        categoryStr = rssItem.split('<title>')[1]
        categoryStr = categoryStr.split('</title>')[0].strip()
        if not categoryStr:
            continue
        if 'CDATA' in categoryStr:
            continue
        hashtagListStr = rssItem.split('<description>')[1]
        hashtagListStr = hashtagListStr.split('</description>')[0].strip()
        if not hashtagListStr:
            continue
        if 'CDATA' in hashtagListStr:
            continue
        hashtagList = hashtagListStr.split(' ')
        if not isBlockedHashtag(baseDir, categoryStr):
            for hashtag in hashtagList:
                setHashtagCategory(baseDir, hashtag, categoryStr, force)


def _xml2StrToDict(baseDir: str, domain: str, xmlStr: str,
                   moderated: bool, mirrored: bool,
                   maxPostsPerSource: int,
                   maxFeedItemSizeKb: int,
                   maxCategoriesFeedItemSizeKb: int) -> {}:
    """Converts an xml RSS 2.0 string to a dictionary
    """
    if '<item>' not in xmlStr:
        return {}
    result = {}

    # is this an rss feed containing hashtag categories?
    if '<title>#categories</title>' in xmlStr:
        _xml2StrToHashtagCategories(baseDir, xmlStr,
                                    maxCategoriesFeedItemSizeKb)
        return {}

    rssItems = xmlStr.split('<item>')
    postCtr = 0
    maxBytes = maxFeedItemSizeKb * 1024
    for rssItem in rssItems:
        if not rssItem:
            continue
        if len(rssItem) > maxBytes:
            print('WARN: rss feed item is too big')
            continue
        if '<title>' not in rssItem:
            continue
        if '</title>' not in rssItem:
            continue
        if '<link>' not in rssItem:
            continue
        if '</link>' not in rssItem:
            continue
        if '<pubDate>' not in rssItem:
            continue
        if '</pubDate>' not in rssItem:
            continue
        title = rssItem.split('<title>')[1]
        title = _removeCDATA(title.split('</title>')[0])
        description = ''
        if '<description>' in rssItem and '</description>' in rssItem:
            description = rssItem.split('<description>')[1]
            description = removeHtml(description.split('</description>')[0])
        else:
            if '<media:description>' in rssItem and \
               '</media:description>' in rssItem:
                description = rssItem.split('<media:description>')[1]
                description = description.split('</media:description>')[0]
                description = removeHtml(description)
        link = rssItem.split('<link>')[1]
        link = link.split('</link>')[0]
        if '://' not in link:
            continue
        itemDomain = link.split('://')[1]
        if '/' in itemDomain:
            itemDomain = itemDomain.split('/')[0]
        if isBlockedDomain(baseDir, itemDomain):
            continue
        pubDate = rssItem.split('<pubDate>')[1]
        pubDate = pubDate.split('</pubDate>')[0]

        pubDateStr = parseFeedDate(pubDate)
        if pubDateStr:
            if _validFeedDate(pubDateStr):
                postFilename = ''
                votesStatus = []
                _addNewswireDictEntry(baseDir, domain,
                                      result, pubDateStr,
                                      title, link,
                                      votesStatus, postFilename,
                                      description, moderated, mirrored)
                postCtr += 1
                if postCtr >= maxPostsPerSource:
                    break
    if postCtr > 0:
        print('Added ' + str(postCtr) + ' rss 2.0 feed items to newswire')
    return result


def _xml1StrToDict(baseDir: str, domain: str, xmlStr: str,
                   moderated: bool, mirrored: bool,
                   maxPostsPerSource: int,
                   maxFeedItemSizeKb: int,
                   maxCategoriesFeedItemSizeKb: int) -> {}:
    """Converts an xml RSS 1.0 string to a dictionary
    https://validator.w3.org/feed/docs/rss1.html
    """
    itemStr = '<item'
    if itemStr not in xmlStr:
        return {}
    result = {}

    # is this an rss feed containing hashtag categories?
    if '<title>#categories</title>' in xmlStr:
        _xml2StrToHashtagCategories(baseDir, xmlStr,
                                    maxCategoriesFeedItemSizeKb)
        return {}

    rssItems = xmlStr.split(itemStr)
    postCtr = 0
    maxBytes = maxFeedItemSizeKb * 1024
    for rssItem in rssItems:
        if not rssItem:
            continue
        if len(rssItem) > maxBytes:
            print('WARN: rss 1.0 feed item is too big')
            continue
        if rssItem.startswith('s>'):
            continue
        if '<title>' not in rssItem:
            continue
        if '</title>' not in rssItem:
            continue
        if '<link>' not in rssItem:
            continue
        if '</link>' not in rssItem:
            continue
        if '<dc:date>' not in rssItem:
            continue
        if '</dc:date>' not in rssItem:
            continue
        title = rssItem.split('<title>')[1]
        title = _removeCDATA(title.split('</title>')[0])
        description = ''
        if '<description>' in rssItem and '</description>' in rssItem:
            description = rssItem.split('<description>')[1]
            description = removeHtml(description.split('</description>')[0])
        else:
            if '<media:description>' in rssItem and \
               '</media:description>' in rssItem:
                description = rssItem.split('<media:description>')[1]
                description = description.split('</media:description>')[0]
                description = removeHtml(description)
        link = rssItem.split('<link>')[1]
        link = link.split('</link>')[0]
        if '://' not in link:
            continue
        itemDomain = link.split('://')[1]
        if '/' in itemDomain:
            itemDomain = itemDomain.split('/')[0]
        if isBlockedDomain(baseDir, itemDomain):
            continue
        pubDate = rssItem.split('<dc:date>')[1]
        pubDate = pubDate.split('</dc:date>')[0]

        pubDateStr = parseFeedDate(pubDate)
        if pubDateStr:
            if _validFeedDate(pubDateStr):
                postFilename = ''
                votesStatus = []
                _addNewswireDictEntry(baseDir, domain,
                                      result, pubDateStr,
                                      title, link,
                                      votesStatus, postFilename,
                                      description, moderated, mirrored)
                postCtr += 1
                if postCtr >= maxPostsPerSource:
                    break
    if postCtr > 0:
        print('Added ' + str(postCtr) + ' rss 1.0 feed items to newswire')
    return result


def _atomFeedToDict(baseDir: str, domain: str, xmlStr: str,
                    moderated: bool, mirrored: bool,
                    maxPostsPerSource: int,
                    maxFeedItemSizeKb: int) -> {}:
    """Converts an atom feed string to a dictionary
    """
    if '<entry>' not in xmlStr:
        return {}
    result = {}
    atomItems = xmlStr.split('<entry>')
    postCtr = 0
    maxBytes = maxFeedItemSizeKb * 1024
    for atomItem in atomItems:
        if not atomItem:
            continue
        if len(atomItem) > maxBytes:
            print('WARN: atom feed item is too big')
            continue
        if '<title>' not in atomItem:
            continue
        if '</title>' not in atomItem:
            continue
        if '<link>' not in atomItem:
            continue
        if '</link>' not in atomItem:
            continue
        if '<updated>' not in atomItem:
            continue
        if '</updated>' not in atomItem:
            continue
        title = atomItem.split('<title>')[1]
        title = _removeCDATA(title.split('</title>')[0])
        description = ''
        if '<summary>' in atomItem and '</summary>' in atomItem:
            description = atomItem.split('<summary>')[1]
            description = removeHtml(description.split('</summary>')[0])
        else:
            if '<media:description>' in atomItem and \
               '</media:description>' in atomItem:
                description = atomItem.split('<media:description>')[1]
                description = description.split('</media:description>')[0]
                description = removeHtml(description)
        link = atomItem.split('<link>')[1]
        link = link.split('</link>')[0]
        if '://' not in link:
            continue
        itemDomain = link.split('://')[1]
        if '/' in itemDomain:
            itemDomain = itemDomain.split('/')[0]
        if isBlockedDomain(baseDir, itemDomain):
            continue
        pubDate = atomItem.split('<updated>')[1]
        pubDate = pubDate.split('</updated>')[0]

        pubDateStr = parseFeedDate(pubDate)
        if pubDateStr:
            if _validFeedDate(pubDateStr):
                postFilename = ''
                votesStatus = []
                _addNewswireDictEntry(baseDir, domain,
                                      result, pubDateStr,
                                      title, link,
                                      votesStatus, postFilename,
                                      description, moderated, mirrored)
                postCtr += 1
                if postCtr >= maxPostsPerSource:
                    break
    if postCtr > 0:
        print('Added ' + str(postCtr) + ' atom feed items to newswire')
    return result


def _atomFeedYTToDict(baseDir: str, domain: str, xmlStr: str,
                      moderated: bool, mirrored: bool,
                      maxPostsPerSource: int,
                      maxFeedItemSizeKb: int) -> {}:
    """Converts an atom-style YouTube feed string to a dictionary
    """
    if '<entry>' not in xmlStr:
        return {}
    if isBlockedDomain(baseDir, 'www.youtube.com'):
        return {}
    result = {}
    atomItems = xmlStr.split('<entry>')
    postCtr = 0
    maxBytes = maxFeedItemSizeKb * 1024
    for atomItem in atomItems:
        if not atomItem:
            continue
        if not atomItem.strip():
            continue
        if len(atomItem) > maxBytes:
            print('WARN: atom feed item is too big')
            continue
        if '<title>' not in atomItem:
            continue
        if '</title>' not in atomItem:
            continue
        if '<published>' not in atomItem:
            continue
        if '</published>' not in atomItem:
            continue
        if '<yt:videoId>' not in atomItem:
            continue
        if '</yt:videoId>' not in atomItem:
            continue
        title = atomItem.split('<title>')[1]
        title = _removeCDATA(title.split('</title>')[0])
        description = ''
        if '<media:description>' in atomItem and \
           '</media:description>' in atomItem:
            description = atomItem.split('<media:description>')[1]
            description = description.split('</media:description>')[0]
            description = removeHtml(description)
        elif '<summary>' in atomItem and '</summary>' in atomItem:
            description = atomItem.split('<summary>')[1]
            description = description.split('</summary>')[0]
            description = removeHtml(description)
        link = atomItem.split('<yt:videoId>')[1]
        link = link.split('</yt:videoId>')[0]
        link = 'https://www.youtube.com/watch?v=' + link.strip()
        pubDate = atomItem.split('<published>')[1]
        pubDate = pubDate.split('</published>')[0]

        pubDateStr = parseFeedDate(pubDate)
        if pubDateStr:
            if _validFeedDate(pubDateStr):
                postFilename = ''
                votesStatus = []
                _addNewswireDictEntry(baseDir, domain,
                                      result, pubDateStr,
                                      title, link,
                                      votesStatus, postFilename,
                                      description, moderated, mirrored)
                postCtr += 1
                if postCtr >= maxPostsPerSource:
                    break
    if postCtr > 0:
        print('Added ' + str(postCtr) + ' YouTube feed items to newswire')
    return result


def _xmlStrToDict(baseDir: str, domain: str, xmlStr: str,
                  moderated: bool, mirrored: bool,
                  maxPostsPerSource: int,
                  maxFeedItemSizeKb: int,
                  maxCategoriesFeedItemSizeKb: int) -> {}:
    """Converts an xml string to a dictionary
    """
    if '<yt:videoId>' in xmlStr and '<yt:channelId>' in xmlStr:
        print('YouTube feed: reading')
        return _atomFeedYTToDict(baseDir, domain,
                                 xmlStr, moderated, mirrored,
                                 maxPostsPerSource, maxFeedItemSizeKb)
    elif 'rss version="2.0"' in xmlStr:
        return _xml2StrToDict(baseDir, domain,
                              xmlStr, moderated, mirrored,
                              maxPostsPerSource, maxFeedItemSizeKb,
                              maxCategoriesFeedItemSizeKb)
    elif '<?xml version="1.0"' in xmlStr:
        return _xml1StrToDict(baseDir, domain,
                              xmlStr, moderated, mirrored,
                              maxPostsPerSource, maxFeedItemSizeKb,
                              maxCategoriesFeedItemSizeKb)
    elif 'xmlns="http://www.w3.org/2005/Atom"' in xmlStr:
        return _atomFeedToDict(baseDir, domain,
                               xmlStr, moderated, mirrored,
                               maxPostsPerSource, maxFeedItemSizeKb)
    return {}


def _YTchannelToAtomFeed(url: str) -> str:
    """Converts a YouTube channel url into an atom feed url
    """
    if 'youtube.com/channel/' not in url:
        return url
    channelId = url.split('youtube.com/channel/')[1].strip()
    channelUrl = \
        'https://www.youtube.com/feeds/videos.xml?channel_id=' + channelId
    print('YouTube feed: ' + channelUrl)
    return channelUrl


def getRSS(baseDir: str, domain: str, session, url: str,
           moderated: bool, mirrored: bool,
           maxPostsPerSource: int, maxFeedSizeKb: int,
           maxFeedItemSizeKb: int,
           maxCategoriesFeedItemSizeKb: int) -> {}:
    """Returns an RSS url as a dict
    """
    if not isinstance(url, str):
        print('url: ' + str(url))
        print('ERROR: getRSS url should be a string')
        return None
    headers = {
        'Accept': 'text/xml, application/xml; charset=UTF-8'
    }
    params = None
    sessionParams = {}
    sessionHeaders = {}
    if headers:
        sessionHeaders = headers
    if params:
        sessionParams = params
    sessionHeaders['User-Agent'] = \
        'Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'
    if not session:
        print('WARN: no session specified for getRSS')
    url = _YTchannelToAtomFeed(url)
    try:
        result = session.get(url, headers=sessionHeaders, params=sessionParams)
        if result:
            if int(len(result.text) / 1024) < maxFeedSizeKb and \
               not containsInvalidChars(result.text):
                return _xmlStrToDict(baseDir, domain, result.text,
                                     moderated, mirrored,
                                     maxPostsPerSource,
                                     maxFeedItemSizeKb,
                                     maxCategoriesFeedItemSizeKb)
            else:
                print('WARN: feed is too large, ' +
                      'or contains invalid characters: ' + url)
        else:
            print('WARN: no result returned for feed ' + url)
    except requests.exceptions.RequestException as e:
        print('ERROR: getRSS failed\nurl: ' + str(url) + '\n' +
              'headers: ' + str(sessionHeaders) + '\n' +
              'params: ' + str(sessionParams) + '\n')
        print(e)
    except ValueError as e:
        print('ERROR: getRSS failed\nurl: ' + str(url) + '\n' +
              'headers: ' + str(sessionHeaders) + '\n' +
              'params: ' + str(sessionParams) + '\n')
        print(e)
    except SocketError as e:
        if e.errno == errno.ECONNRESET:
            print('WARN: connection was reset during getRSS')
        print(e)
    return None


def getRSSfromDict(baseDir: str, newswire: {},
                   httpPrefix: str, domainFull: str,
                   title: str, translate: {}) -> str:
    """Returns an rss feed from the current newswire dict.
    This allows other instances to subscribe to the same newswire
    """
    rssStr = rss2Header(httpPrefix,
                        None, domainFull,
                        'Newswire', translate)
    if not newswire:
        return ''
    for published, fields in newswire.items():
        if '+00:00' in published:
            published = published.replace('+00:00', 'Z').strip()
            published = published.replace(' ', 'T')
        else:
            publishedWithOffset = \
                datetime.strptime(published, "%Y-%m-%d %H:%M:%S%z")
            published = publishedWithOffset.strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            pubDate = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
        except Exception as e:
            print('WARN: Unable to convert date ' + published + ' ' + str(e))
            continue
        rssStr += '<item>\n'
        rssStr += '  <title>' + fields[0] + '</title>\n'
        description = removeHtml(firstParagraphFromString(fields[4]))
        rssStr += '  <description>' + description + '</description>\n'
        url = fields[1]
        if '://' not in url:
            if domainFull not in url:
                url = httpPrefix + '://' + domainFull + url
        rssStr += '  <link>' + url + '</link>\n'

        rssDateStr = pubDate.strftime("%a, %d %b %Y %H:%M:%S UT")
        rssStr += '  <pubDate>' + rssDateStr + '</pubDate>\n'
        rssStr += '</item>\n'
    rssStr += rss2Footer()
    return rssStr


def _isNewswireBlogPost(postJsonObject: {}) -> bool:
    """Is the given object a blog post?
    There isn't any difference between a blog post and a newswire blog post
    but we may here need to check for different properties than
    isBlogPost does
    """
    if not postJsonObject:
        return False
    if not postJsonObject.get('object'):
        return False
    if not isinstance(postJsonObject['object'], dict):
        return False
    if postJsonObject['object'].get('summary') and \
       postJsonObject['object'].get('url') and \
       postJsonObject['object'].get('content') and \
       postJsonObject['object'].get('published'):
        return isPublicPost(postJsonObject)
    return False


def _getHashtagsFromPost(postJsonObject: {}) -> []:
    """Returns a list of any hashtags within a post
    """
    if not postJsonObject.get('object'):
        return []
    if not isinstance(postJsonObject['object'], dict):
        return []
    if not postJsonObject['object'].get('tag'):
        return []
    if not isinstance(postJsonObject['object']['tag'], list):
        return []
    tags = []
    for tg in postJsonObject['object']['tag']:
        if not isinstance(tg, dict):
            continue
        if not tg.get('name'):
            continue
        if not tg.get('type'):
            continue
        if tg['type'] != 'Hashtag':
            continue
        if tg['name'] not in tags:
            tags.append(tg['name'])
    return tags


def _addAccountBlogsToNewswire(baseDir: str, nickname: str, domain: str,
                               newswire: {},
                               maxBlogsPerAccount: int,
                               indexFilename: str,
                               maxTags: int) -> None:
    """Adds blogs for the given account to the newswire
    """
    if not os.path.isfile(indexFilename):
        return
    # local blog entries are unmoderated by default
    moderated = False

    # local blogs can potentially be moderated
    moderatedFilename = \
        baseDir + '/accounts/' + nickname + '@' + domain + \
        '/.newswiremoderated'
    if os.path.isfile(moderatedFilename):
        moderated = True

    with open(indexFilename, 'r') as indexFile:
        postFilename = 'start'
        ctr = 0
        while postFilename:
            postFilename = indexFile.readline()
            if postFilename:
                # if this is a full path then remove the directories
                if '/' in postFilename:
                    postFilename = postFilename.split('/')[-1]

                # filename of the post without any extension or path
                # This should also correspond to any index entry in
                # the posts cache
                postUrl = \
                    postFilename.replace('\n', '').replace('\r', '')
                postUrl = postUrl.replace('.json', '').strip()

                # read the post from file
                fullPostFilename = \
                    locatePost(baseDir, nickname,
                               domain, postUrl, False)
                if not fullPostFilename:
                    print('Unable to locate post ' + postUrl)
                    ctr += 1
                    if ctr >= maxBlogsPerAccount:
                        break
                    continue

                postJsonObject = None
                if fullPostFilename:
                    postJsonObject = loadJson(fullPostFilename)
                if _isNewswireBlogPost(postJsonObject):
                    published = postJsonObject['object']['published']
                    published = published.replace('T', ' ')
                    published = published.replace('Z', '+00:00')
                    votes = []
                    if os.path.isfile(fullPostFilename + '.votes'):
                        votes = loadJson(fullPostFilename + '.votes')
                    content = postJsonObject['object']['content']
                    description = firstParagraphFromString(content)
                    description = removeHtml(description)
                    tagsFromPost = _getHashtagsFromPost(postJsonObject)
                    _addNewswireDictEntry(baseDir, domain,
                                          newswire, published,
                                          postJsonObject['object']['summary'],
                                          postJsonObject['object']['url'],
                                          votes, fullPostFilename,
                                          description, moderated, False,
                                          tagsFromPost,
                                          maxTags)

            ctr += 1
            if ctr >= maxBlogsPerAccount:
                break


def _addBlogsToNewswire(baseDir: str, domain: str, newswire: {},
                        maxBlogsPerAccount: int,
                        maxTags: int) -> None:
    """Adds blogs from each user account into the newswire
    """
    moderationDict = {}

    # go through each account
    for subdir, dirs, files in os.walk(baseDir + '/accounts'):
        for handle in dirs:
            if '@' not in handle:
                continue
            if 'inbox@' in handle:
                continue

            nickname = handle.split('@')[0]

            # has this account been suspended?
            if isSuspended(baseDir, nickname):
                continue

            if os.path.isfile(baseDir + '/accounts/' + handle +
                              '/.nonewswire'):
                continue

            # is there a blogs timeline for this account?
            accountDir = os.path.join(baseDir + '/accounts', handle)
            blogsIndex = accountDir + '/tlblogs.index'
            if os.path.isfile(blogsIndex):
                domain = handle.split('@')[1]
                _addAccountBlogsToNewswire(baseDir, nickname, domain,
                                           newswire, maxBlogsPerAccount,
                                           blogsIndex, maxTags)
        break

    # sort the moderation dict into chronological order, latest first
    sortedModerationDict = \
        OrderedDict(sorted(moderationDict.items(), reverse=True))
    # save the moderation queue details for later display
    newswireModerationFilename = baseDir + '/accounts/newswiremoderation.txt'
    if sortedModerationDict:
        saveJson(sortedModerationDict, newswireModerationFilename)
    else:
        # remove the file if there is nothing to moderate
        if os.path.isfile(newswireModerationFilename):
            os.remove(newswireModerationFilename)


def getDictFromNewswire(session, baseDir: str, domain: str,
                        maxPostsPerSource: int, maxFeedSizeKb: int,
                        maxTags: int, maxFeedItemSizeKb: int,
                        maxNewswirePosts: int,
                        maxCategoriesFeedItemSizeKb: int) -> {}:
    """Gets rss feeds as a dictionary from newswire file
    """
    subscriptionsFilename = baseDir + '/accounts/newswire.txt'
    if not os.path.isfile(subscriptionsFilename):
        return {}

    maxPostsPerSource = 5

    # add rss feeds
    rssFeed = []
    with open(subscriptionsFilename, 'r') as fp:
        rssFeed = fp.readlines()
    result = {}
    for url in rssFeed:
        url = url.strip()

        # Does this contain a url?
        if '://' not in url:
            continue

        # is this a comment?
        if url.startswith('#'):
            continue

        # should this feed be moderated?
        moderated = False
        if '*' in url:
            moderated = True
            url = url.replace('*', '').strip()

        # should this feed content be mirrored?
        mirrored = False
        if '!' in url:
            mirrored = True
            url = url.replace('!', '').strip()

        itemsList = getRSS(baseDir, domain, session, url,
                           moderated, mirrored,
                           maxPostsPerSource, maxFeedSizeKb,
                           maxFeedItemSizeKb,
                           maxCategoriesFeedItemSizeKb)
        if itemsList:
            for dateStr, item in itemsList.items():
                result[dateStr] = item

    # add blogs from each user account
    _addBlogsToNewswire(baseDir, domain, result,
                        maxPostsPerSource, maxTags)

    # sort into chronological order, latest first
    sortedResult = OrderedDict(sorted(result.items(), reverse=True))

    # are there too many posts? If so then remove the oldest ones
    noOfPosts = len(sortedResult.items())
    if noOfPosts > maxNewswirePosts:
        ctr = 0
        removals = []
        for dateStr, item in sortedResult.items():
            ctr += 1
            if ctr > maxNewswirePosts:
                removals.append(dateStr)
        for r in removals:
            sortedResult.pop(r)

    return sortedResult
