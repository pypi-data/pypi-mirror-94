__filename__ = "webapp_column_right.py"
__author__ = "Bob Mottram"
__license__ = "AGPL3+"
__version__ = "1.2.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@freedombone.net"
__status__ = "Production"

import os
from datetime import datetime
from content import removeLongWords
from utils import removeHtml
from utils import locatePost
from utils import loadJson
from utils import votesOnNewswireItem
from utils import getNicknameFromActor
from utils import isEditor
from utils import getConfigParam
from posts import isModerator
from webapp_utils import getRightImageFile
from webapp_utils import htmlHeaderWithExternalStyle
from webapp_utils import htmlFooter
from webapp_utils import getBannerFile
from webapp_utils import htmlPostSeparator
from webapp_utils import headerButtonsFrontScreen


def _votesIndicator(totalVotes: int, positiveVoting: bool) -> str:
    """Returns an indicator of the number of votes on a newswire item
    """
    if totalVotes <= 0:
        return ''
    totalVotesStr = ' '
    for v in range(totalVotes):
        if positiveVoting:
            totalVotesStr += '✓'
        else:
            totalVotesStr += '✗'
    return totalVotesStr


def getRightColumnContent(baseDir: str, nickname: str, domainFull: str,
                          httpPrefix: str, translate: {},
                          moderator: bool, editor: bool,
                          newswire: {}, positiveVoting: bool,
                          showBackButton: bool, timelinePath: str,
                          showPublishButton: bool,
                          showPublishAsIcon: bool,
                          rssIconAtTop: bool,
                          publishButtonAtTop: bool,
                          authorized: bool,
                          showHeaderImage: bool,
                          theme: str,
                          defaultTimeline: str) -> str:
    """Returns html content for the right column
    """
    htmlStr = ''

    domain = domainFull
    if ':' in domain:
        domain = domain.split(':')

    if authorized:
        # only show the publish button if logged in, otherwise replace it with
        # a login button
        titleStr = translate['Publish a blog article']
        if defaultTimeline == 'tlfeatures':
            titleStr = translate['Publish a news article']
        publishButtonStr = \
            '        <a href="' + \
            '/users/' + nickname + '/newblog?nodropdown" ' + \
            'title="' + titleStr + '">' + \
            '<button class="publishbtn">' + \
            translate['Publish'] + '</button></a>\n'
    else:
        # if not logged in then replace the publish button with
        # a login button
        publishButtonStr = \
            '        <a href="/login"><button class="publishbtn">' + \
            translate['Login'] + '</button></a>\n'

    # show publish button at the top if needed
    if publishButtonAtTop:
        htmlStr += '<center>' + publishButtonStr + '</center>'

    # show a column header image, eg. title of the theme or newswire banner
    editImageClass = ''
    if showHeaderImage:
        rightImageFile, rightColumnImageFilename = \
            getRightImageFile(baseDir, nickname, domain, theme)

        # show the image at the top of the column
        editImageClass = 'rightColEdit'
        if os.path.isfile(rightColumnImageFilename):
            editImageClass = 'rightColEditImage'
            htmlStr += \
                '\n      <center>\n' + \
                '          <img class="rightColImg" ' + \
                'alt="" loading="lazy" src="/users/' + \
                nickname + '/' + rightImageFile + '" />\n' + \
                '      </center>\n'

    if (showPublishButton or editor or rssIconAtTop) and not showHeaderImage:
        htmlStr += '<div class="columnIcons">'

    if editImageClass == 'rightColEdit':
        htmlStr += '\n      <center>\n'

    # whether to show a back icon
    # This is probably going to be osolete soon
    if showBackButton:
        htmlStr += \
            '      <a href="' + timelinePath + '">' + \
            '<button class="cancelbtn">' + \
            translate['Go Back'] + '</button></a>\n'

    if showPublishButton and not publishButtonAtTop:
        if not showPublishAsIcon:
            htmlStr += publishButtonStr

    # show the edit icon
    if editor:
        if os.path.isfile(baseDir + '/accounts/newswiremoderation.txt'):
            # show the edit icon highlighted
            htmlStr += \
                '        <a href="' + \
                '/users/' + nickname + '/editnewswire">' + \
                '<img class="' + editImageClass + \
                '" loading="lazy" alt="' + \
                translate['Edit newswire'] + ' | " title="' + \
                translate['Edit newswire'] + '" src="/' + \
                'icons/edit_notify.png" /></a>\n'
        else:
            # show the edit icon
            htmlStr += \
                '        <a href="' + \
                '/users/' + nickname + '/editnewswire">' + \
                '<img class="' + editImageClass + \
                '" loading="lazy" alt="' + \
                translate['Edit newswire'] + ' | " title="' + \
                translate['Edit newswire'] + '" src="/' + \
                'icons/edit.png" /></a>\n'

    # show the RSS icons
    rssIconStr = \
        '        <a href="/categories.xml">' + \
        '<img class="' + editImageClass + \
        '" loading="lazy" alt="' + \
        translate['Hashtag Categories RSS Feed'] + ' | " title="' + \
        translate['Hashtag Categories RSS Feed'] + '" src="/' + \
        'icons/categoriesrss.png" /></a>\n'
    rssIconStr += \
        '        <a href="/newswire.xml">' + \
        '<img class="' + editImageClass + \
        '" loading="lazy" alt="' + \
        translate['Newswire RSS Feed'] + ' | " title="' + \
        translate['Newswire RSS Feed'] + '" src="/' + \
        'icons/logorss.png" /></a>\n'
    if rssIconAtTop:
        htmlStr += rssIconStr

    # show publish icon at top
    if showPublishButton:
        if showPublishAsIcon:
            titleStr = translate['Publish a blog article']
            if defaultTimeline == 'tlfeatures':
                titleStr = translate['Publish a news article']
            htmlStr += \
                '        <a href="' + \
                '/users/' + nickname + '/newblog?nodropdown">' + \
                '<img class="' + editImageClass + \
                '" loading="lazy" alt="' + \
                titleStr + '" title="' + \
                titleStr + '" src="/' + \
                'icons/publish.png" /></a>\n'

    if editImageClass == 'rightColEdit':
        htmlStr += '      </center>\n'
    else:
        if showHeaderImage:
            htmlStr += '      <br>\n'

    if (showPublishButton or editor or rssIconAtTop) and not showHeaderImage:
        htmlStr += '</div><br>'

    # show the newswire lines
    newswireContentStr = \
        _htmlNewswire(baseDir, newswire, nickname, moderator, translate,
                      positiveVoting)
    htmlStr += newswireContentStr

    # show the rss icon at the bottom, typically on the right hand side
    if newswireContentStr and not rssIconAtTop:
        htmlStr += '<br><div class="columnIcons">' + rssIconStr + '</div>'
    return htmlStr


def _getBrokenFavSubstitute() -> str:
    """Substitute link used if a favicon is not available
    """
    return " onerror=\"this.onerror=null; this.src='/newswire_favicon.ico'\""


def _getNewswireFavicon(url: str) -> str:
    """Returns a favicon url from the given article link
    """
    if '://' not in url:
        return '/newswire_favicon.ico'
    if url.startswith('http://'):
        if not (url.endswith('.onion') or url.endswith('.i2p')):
            return '/newswire_favicon.ico'
    domain = url.split('://')[1]
    if '/' not in domain:
        return url + '/favicon.ico'
    else:
        domain = domain.split('/')[0]
    return url.split('://')[0] + '://' + domain + '/favicon.ico'


def _htmlNewswire(baseDir: str, newswire: {}, nickname: str, moderator: bool,
                  translate: {}, positiveVoting: bool) -> str:
    """Converts a newswire dict into html
    """
    separatorStr = htmlPostSeparator(baseDir, 'right')
    htmlStr = ''
    for dateStr, item in newswire.items():
        item[0] = removeHtml(item[0]).strip()
        if not item[0]:
            continue
        # remove any CDATA
        if 'CDATA[' in item[0]:
            item[0] = item[0].split('CDATA[')[1]
            if ']' in item[0]:
                item[0] = item[0].split(']')[0]
        try:
            publishedDate = \
                datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S%z")
        except BaseException:
            print('WARN: bad date format ' + dateStr)
            continue
        dateShown = publishedDate.strftime("%Y-%m-%d %H:%M")

        dateStrLink = dateStr.replace('T', ' ')
        dateStrLink = dateStrLink.replace('Z', '')
        url = item[1]
        faviconUrl = _getNewswireFavicon(url)
        faviconLink = ''
        if faviconUrl:
            faviconLink = \
                '<img loading="lazy" src="' + faviconUrl + '" ' + \
                'alt="" ' + \
                _getBrokenFavSubstitute() + '/>'
        moderatedItem = item[5]
        htmlStr += separatorStr
        if moderatedItem and 'vote:' + nickname in item[2]:
            totalVotesStr = ''
            totalVotes = 0
            if moderator:
                totalVotes = votesOnNewswireItem(item[2])
                totalVotesStr = \
                    _votesIndicator(totalVotes, positiveVoting)

            title = removeLongWords(item[0], 16, []).replace('\n', '<br>')
            htmlStr += '<p class="newswireItemVotedOn">' + \
                '<a href="' + url + '" target="_blank" ' + \
                'rel="nofollow noopener noreferrer">' + \
                '<span class="newswireItemVotedOn">' + \
                faviconLink + title + \
                '</span></a>' + totalVotesStr
            if moderator:
                htmlStr += \
                    ' ' + dateShown + '<a href="/users/' + nickname + \
                    '/newswireunvote=' + dateStrLink + '" ' + \
                    'title="' + translate['Remove Vote'] + '">'
                htmlStr += '<img loading="lazy" class="voteicon" src="/' + \
                    'alt="' + translate['Remove Vote'] + '" ' + \
                    'icons/vote.png" /></a></p>\n'
            else:
                htmlStr += ' <span class="newswireDateVotedOn">'
                htmlStr += dateShown + '</span></p>\n'
        else:
            totalVotesStr = ''
            totalVotes = 0
            if moderator:
                if moderatedItem:
                    totalVotes = votesOnNewswireItem(item[2])
                    # show a number of ticks or crosses for how many
                    # votes for or against
                    totalVotesStr = \
                        _votesIndicator(totalVotes, positiveVoting)

            title = removeLongWords(item[0], 16, []).replace('\n', '<br>')
            if moderator and moderatedItem:
                htmlStr += '<p class="newswireItemModerated">' + \
                    '<a href="' + url + '" target="_blank" ' + \
                    'rel="nofollow noopener noreferrer">' + \
                    faviconLink + title + '</a>' + totalVotesStr
                htmlStr += ' ' + dateShown
                htmlStr += '<a href="/users/' + nickname + \
                    '/newswirevote=' + dateStrLink + '" ' + \
                    'title="' + translate['Vote'] + '">'
                htmlStr += '<img class="voteicon" ' + \
                    'alt="' + translate['Vote'] + '" ' + \
                    'src="/icons/vote.png" /></a>'
                htmlStr += '</p>\n'
            else:
                htmlStr += '<p class="newswireItem">' + \
                    '<a href="' + url + '" target="_blank" ' + \
                    'rel="nofollow noopener noreferrer">' + \
                    faviconLink + title + '</a>' + \
                    totalVotesStr
                htmlStr += ' <span class="newswireDate">'
                htmlStr += dateShown + '</span></p>\n'

    if htmlStr:
        htmlStr = '<nav>\n' + htmlStr + '</nav>\n'
    return htmlStr


def htmlCitations(baseDir: str, nickname: str, domain: str,
                  httpPrefix: str, defaultTimeline: str,
                  translate: {}, newswire: {}, cssCache: {},
                  blogTitle: str, blogContent: str,
                  blogImageFilename: str,
                  blogImageAttachmentMediaType: str,
                  blogImageDescription: str,
                  theme: str) -> str:
    """Show the citations screen when creating a blog
    """
    htmlStr = ''

    # create a list of dates for citations
    # these can then be used to re-select checkboxes later
    citationsFilename = \
        baseDir + '/accounts/' + \
        nickname + '@' + domain + '/.citations.txt'
    citationsSelected = []
    if os.path.isfile(citationsFilename):
        citationsSeparator = '#####'
        with open(citationsFilename, "r") as f:
            citations = f.readlines()
            for line in citations:
                if citationsSeparator not in line:
                    continue
                sections = line.strip().split(citationsSeparator)
                if len(sections) != 3:
                    continue
                dateStr = sections[0]
                citationsSelected.append(dateStr)

    # the css filename
    cssFilename = baseDir + '/epicyon-profile.css'
    if os.path.isfile(baseDir + '/epicyon.css'):
        cssFilename = baseDir + '/epicyon.css'

    instanceTitle = \
        getConfigParam(baseDir, 'instanceTitle')
    htmlStr = htmlHeaderWithExternalStyle(cssFilename, instanceTitle)

    # top banner
    bannerFile, bannerFilename = \
        getBannerFile(baseDir, nickname, domain, theme)
    htmlStr += \
        '<a href="/users/' + nickname + '/newblog" title="' + \
        translate['Go Back'] + '" alt="' + \
        translate['Go Back'] + '">\n'
    htmlStr += '<img loading="lazy" class="timeline-banner" ' + \
        'alt="" src="' + \
        '/users/' + nickname + '/' + bannerFile + '" /></a>\n'

    htmlStr += \
        '<form enctype="multipart/form-data" method="POST" ' + \
        'accept-charset="UTF-8" action="/users/' + nickname + \
        '/citationsdata">\n'
    htmlStr += '  <center>\n'
    htmlStr += translate['Choose newswire items ' +
                         'referenced in your article'] + '<br>'
    if blogTitle is None:
        blogTitle = ''
    htmlStr += \
        '    <input type="hidden" name="blogTitle" value="' + \
        blogTitle + '">\n'
    if blogContent is None:
        blogContent = ''
    htmlStr += \
        '    <input type="hidden" name="blogContent" value="' + \
        blogContent + '">\n'
    # submit button
    htmlStr += \
        '    <input type="submit" name="submitCitations" value="' + \
        translate['Submit'] + '">\n'
    htmlStr += '  </center>\n'

    citationsSeparator = '#####'

    # list of newswire items
    if newswire:
        ctr = 0
        for dateStr, item in newswire.items():
            item[0] = removeHtml(item[0]).strip()
            if not item[0]:
                continue
            # remove any CDATA
            if 'CDATA[' in item[0]:
                item[0] = item[0].split('CDATA[')[1]
                if ']' in item[0]:
                    item[0] = item[0].split(']')[0]
            # should this checkbox be selected?
            selectedStr = ''
            if dateStr in citationsSelected:
                selectedStr = ' checked'

            publishedDate = \
                datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S%z")
            dateShown = publishedDate.strftime("%Y-%m-%d %H:%M")

            title = removeLongWords(item[0], 16, []).replace('\n', '<br>')
            link = item[1]

            citationValue = \
                dateStr + citationsSeparator + \
                title + citationsSeparator + \
                link
            htmlStr += \
                '<input type="checkbox" name="newswire' + str(ctr) + \
                '" value="' + citationValue + '"' + selectedStr + '/>' + \
                '<a href="' + link + '"><cite>' + title + '</cite></a> '
            htmlStr += '<span class="newswireDate">' + \
                dateShown + '</span><br>\n'
            ctr += 1

    htmlStr += '</form>\n'
    return htmlStr + htmlFooter()


def htmlNewswireMobile(cssCache: {}, baseDir: str, nickname: str,
                       domain: str, domainFull: str,
                       httpPrefix: str, translate: {},
                       newswire: {},
                       positiveVoting: bool,
                       timelinePath: str,
                       showPublishAsIcon: bool,
                       authorized: bool,
                       rssIconAtTop: bool,
                       iconsAsButtons: bool,
                       defaultTimeline: str,
                       theme: str) -> str:
    """Shows the mobile version of the newswire right column
    """
    htmlStr = ''

    # the css filename
    cssFilename = baseDir + '/epicyon-profile.css'
    if os.path.isfile(baseDir + '/epicyon.css'):
        cssFilename = baseDir + '/epicyon.css'

    if nickname == 'news':
        editor = False
        moderator = False
    else:
        # is the user a moderator?
        moderator = isModerator(baseDir, nickname)

        # is the user a site editor?
        editor = isEditor(baseDir, nickname)

    showPublishButton = editor

    instanceTitle = \
        getConfigParam(baseDir, 'instanceTitle')
    htmlStr = htmlHeaderWithExternalStyle(cssFilename, instanceTitle)

    bannerFile, bannerFilename = \
        getBannerFile(baseDir, nickname, domain, theme)
    htmlStr += \
        '<a href="/users/' + nickname + '/' + defaultTimeline + '">' + \
        '<img loading="lazy" class="timeline-banner" ' + \
        'alt="' + translate['Timeline banner image'] + '" ' + \
        'src="/users/' + nickname + '/' + bannerFile + '" /></a>\n'

    htmlStr += '<div class="col-right-mobile">\n'

    htmlStr += '<center>' + \
        headerButtonsFrontScreen(translate, nickname,
                                 'newswire', authorized,
                                 iconsAsButtons) + '</center>'
    if newswire:
        htmlStr += \
            getRightColumnContent(baseDir, nickname, domainFull,
                                  httpPrefix, translate,
                                  moderator, editor,
                                  newswire, positiveVoting,
                                  False, timelinePath, showPublishButton,
                                  showPublishAsIcon, rssIconAtTop, False,
                                  authorized, False, theme,
                                  defaultTimeline)
    else:
        if editor:
            htmlStr += '<br><br><br>\n'
            htmlStr += '<center>\n  '
            htmlStr += translate['Select the edit icon to add RSS feeds']
            htmlStr += '\n</center>\n'
    # end of col-right-mobile
    htmlStr += '</div\n>'

    htmlStr += htmlFooter()
    return htmlStr


def htmlEditNewswire(cssCache: {}, translate: {}, baseDir: str, path: str,
                     domain: str, port: int, httpPrefix: str,
                     defaultTimeline: str, theme: str) -> str:
    """Shows the edit newswire screen
    """
    if '/users/' not in path:
        return ''
    path = path.replace('/inbox', '').replace('/outbox', '')
    path = path.replace('/shares', '')

    nickname = getNicknameFromActor(path)
    if not nickname:
        return ''

    # is the user a moderator?
    if not isModerator(baseDir, nickname):
        return ''

    cssFilename = baseDir + '/epicyon-links.css'
    if os.path.isfile(baseDir + '/links.css'):
        cssFilename = baseDir + '/links.css'

    # filename of the banner shown at the top
    bannerFile, bannerFilename = \
        getBannerFile(baseDir, nickname, domain, theme)

    instanceTitle = \
        getConfigParam(baseDir, 'instanceTitle')
    editNewswireForm = htmlHeaderWithExternalStyle(cssFilename, instanceTitle)

    # top banner
    editNewswireForm += \
        '<header>' + \
        '<a href="/users/' + nickname + '/' + defaultTimeline + '" title="' + \
        translate['Switch to timeline view'] + '" alt="' + \
        translate['Switch to timeline view'] + '">\n'
    editNewswireForm += '<img loading="lazy" class="timeline-banner" src="' + \
        '/users/' + nickname + '/' + bannerFile + '" ' + \
        'alt="" /></a>\n</header>'

    editNewswireForm += \
        '<form enctype="multipart/form-data" method="POST" ' + \
        'accept-charset="UTF-8" action="' + path + '/newswiredata">\n'
    editNewswireForm += \
        '  <div class="vertical-center">\n'
    editNewswireForm += \
        '    <h1>' + translate['Edit newswire'] + '</h1>'
    editNewswireForm += \
        '    <div class="containerSubmitNewPost">\n'
    editNewswireForm += \
        '      <input type="submit" name="submitNewswire" value="' + \
        translate['Submit'] + '">\n'
    editNewswireForm += \
        '    </div>\n'

    newswireFilename = baseDir + '/accounts/newswire.txt'
    newswireStr = ''
    if os.path.isfile(newswireFilename):
        with open(newswireFilename, 'r') as fp:
            newswireStr = fp.read()

    editNewswireForm += \
        '<div class="container">'

    editNewswireForm += \
        '  ' + \
        translate['Add RSS feed links below.'] + \
        '<br>'
    editNewswireForm += \
        '  <textarea id="message" name="editedNewswire" ' + \
        'style="height:80vh">' + newswireStr + '</textarea>'

    filterStr = ''
    filterFilename = \
        baseDir + '/accounts/news@' + domain + '/filters.txt'
    if os.path.isfile(filterFilename):
        with open(filterFilename, 'r') as filterfile:
            filterStr = filterfile.read()

    editNewswireForm += \
        '      <br><b><label class="labels">' + \
        translate['Filtered words'] + '</label></b>\n'
    editNewswireForm += '      <br><label class="labels">' + \
        translate['One per line'] + '</label>'
    editNewswireForm += '      <textarea id="message" ' + \
        'name="filteredWordsNewswire" style="height:50vh">' + \
        filterStr + '</textarea>\n'

    hashtagRulesStr = ''
    hashtagRulesFilename = \
        baseDir + '/accounts/hashtagrules.txt'
    if os.path.isfile(hashtagRulesFilename):
        with open(hashtagRulesFilename, 'r') as rulesfile:
            hashtagRulesStr = rulesfile.read()

    editNewswireForm += \
        '      <br><b><label class="labels">' + \
        translate['News tagging rules'] + '</label></b>\n'
    editNewswireForm += '      <br><label class="labels">' + \
        translate['One per line'] + '.</label>\n'
    editNewswireForm += \
        '      <a href="' + \
        'https://gitlab.com/bashrc2/epicyon/-/raw/main/hashtagrules.txt' + \
        '">' + translate['See instructions'] + '</a>\n'
    editNewswireForm += '      <textarea id="message" ' + \
        'name="hashtagRulesList" style="height:80vh">' + \
        hashtagRulesStr + '</textarea>\n'

    editNewswireForm += \
        '</div>'

    editNewswireForm += htmlFooter()
    return editNewswireForm


def htmlEditNewsPost(cssCache: {}, translate: {}, baseDir: str, path: str,
                     domain: str, port: int,
                     httpPrefix: str, postUrl: str) -> str:
    """Edits a news post on the news/features timeline
    """
    if '/users/' not in path:
        return ''
    pathOriginal = path

    nickname = getNicknameFromActor(path)
    if not nickname:
        return ''

    # is the user an editor?
    if not isEditor(baseDir, nickname):
        return ''

    postUrl = postUrl.replace('/', '#')
    postFilename = locatePost(baseDir, nickname, domain, postUrl)
    if not postFilename:
        return ''
    postJsonObject = loadJson(postFilename)
    if not postJsonObject:
        return ''

    cssFilename = baseDir + '/epicyon-links.css'
    if os.path.isfile(baseDir + '/links.css'):
        cssFilename = baseDir + '/links.css'

    instanceTitle = \
        getConfigParam(baseDir, 'instanceTitle')
    editNewsPostForm = htmlHeaderWithExternalStyle(cssFilename, instanceTitle)
    editNewsPostForm += \
        '<form enctype="multipart/form-data" method="POST" ' + \
        'accept-charset="UTF-8" action="' + path + '/newseditdata">\n'
    editNewsPostForm += \
        '  <div class="vertical-center">\n'
    editNewsPostForm += \
        '    <h1>' + translate['Edit News Post'] + '</h1>'
    editNewsPostForm += \
        '    <div class="container">\n'
    editNewsPostForm += \
        '      <a href="' + pathOriginal + '/tlnews">' + \
        '<button class="cancelbtn">' + translate['Go Back'] + '</button></a>\n'
    editNewsPostForm += \
        '      <input type="submit" name="submitEditedNewsPost" value="' + \
        translate['Submit'] + '">\n'
    editNewsPostForm += \
        '    </div>\n'

    editNewsPostForm += \
        '<div class="container">'

    editNewsPostForm += \
        '  <input type="hidden" name="newsPostUrl" value="' + \
        postUrl + '">\n'

    newsPostTitle = postJsonObject['object']['summary']
    editNewsPostForm += \
        '  <input type="text" name="newsPostTitle" value="' + \
        newsPostTitle + '"><br>\n'

    newsPostContent = postJsonObject['object']['content']
    editNewsPostForm += \
        '  <textarea id="message" name="editedNewsPost" ' + \
        'style="height:600px">' + newsPostContent + '</textarea>'

    editNewsPostForm += \
        '</div>'

    editNewsPostForm += htmlFooter()
    return editNewsPostForm
