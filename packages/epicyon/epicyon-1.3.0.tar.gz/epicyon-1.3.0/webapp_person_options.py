__filename__ = "webapp_person_options.py"
__author__ = "Bob Mottram"
__license__ = "AGPL3+"
__version__ = "1.2.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@freedombone.net"
__status__ = "Production"

import os
from shutil import copyfile
from petnames import getPetName
from person import isPersonSnoozed
from posts import isModerator
from utils import getFullDomain
from utils import getConfigParam
from utils import isDormant
from utils import removeHtml
from utils import getDomainFromActor
from utils import getNicknameFromActor
from blocking import isBlocked
from follow import isFollowerOfPerson
from follow import isFollowingActor
from followingCalendar import receivingCalendarEvents
from webapp_utils import htmlHeaderWithExternalStyle
from webapp_utils import htmlFooter
from webapp_utils import getBrokenLinkSubstitute


def htmlPersonOptions(defaultTimeline: str,
                      cssCache: {}, translate: {}, baseDir: str,
                      domain: str, domainFull: str,
                      originPathStr: str,
                      optionsActor: str,
                      optionsProfileUrl: str,
                      optionsLink: str,
                      pageNumber: int,
                      donateUrl: str,
                      xmppAddress: str,
                      matrixAddress: str,
                      ssbAddress: str,
                      blogAddress: str,
                      toxAddress: str,
                      briarAddress: str,
                      jamiAddress: str,
                      PGPpubKey: str,
                      PGPfingerprint: str,
                      emailAddress: str,
                      dormantMonths: int,
                      backToPath: str,
                      lockedAccount: bool,
                      movedTo: str,
                      alsoKnownAs: []) -> str:
    """Show options for a person: view/follow/block/report
    """
    optionsDomain, optionsPort = getDomainFromActor(optionsActor)
    optionsDomainFull = getFullDomain(optionsDomain, optionsPort)

    if os.path.isfile(baseDir + '/accounts/options-background-custom.jpg'):
        if not os.path.isfile(baseDir + '/accounts/options-background.jpg'):
            copyfile(baseDir + '/accounts/options-background.jpg',
                     baseDir + '/accounts/options-background.jpg')

    dormant = False
    followStr = 'Follow'
    blockStr = 'Block'
    nickname = None
    optionsNickname = None
    followsYou = False
    if originPathStr.startswith('/users/'):
        nickname = originPathStr.split('/users/')[1]
        if '/' in nickname:
            nickname = nickname.split('/')[0]
        if '?' in nickname:
            nickname = nickname.split('?')[0]
        followerDomain, followerPort = getDomainFromActor(optionsActor)
        if isFollowingActor(baseDir, nickname, domain, optionsActor):
            followStr = 'Unfollow'
            dormant = \
                isDormant(baseDir, nickname, domain, optionsActor,
                          dormantMonths)

        optionsNickname = getNicknameFromActor(optionsActor)
        optionsDomainFull = getFullDomain(optionsDomain, optionsPort)
        followsYou = \
            isFollowerOfPerson(baseDir,
                               nickname, domain,
                               optionsNickname, optionsDomainFull)
        if isBlocked(baseDir, nickname, domain,
                     optionsNickname, optionsDomainFull):
            blockStr = 'Block'

    optionsLinkStr = ''
    if optionsLink:
        optionsLinkStr = \
            '    <input type="hidden" name="postUrl" value="' + \
            optionsLink + '">\n'
    cssFilename = baseDir + '/epicyon-options.css'
    if os.path.isfile(baseDir + '/options.css'):
        cssFilename = baseDir + '/options.css'

    # To snooze, or not to snooze? That is the question
    snoozeButtonStr = 'Snooze'
    if nickname:
        if isPersonSnoozed(baseDir, nickname, domain, optionsActor):
            snoozeButtonStr = 'Unsnooze'

    donateStr = ''
    if donateUrl:
        donateStr = \
            '    <a href="' + donateUrl + \
            '"><button class="button" name="submitDonate">' + \
            translate['Donate'] + '</button></a>\n'

    instanceTitle = \
        getConfigParam(baseDir, 'instanceTitle')
    optionsStr = htmlHeaderWithExternalStyle(cssFilename, instanceTitle)
    optionsStr += '<br><br>\n'
    optionsStr += '<div class="options">\n'
    optionsStr += '  <div class="optionsAvatar">\n'
    optionsStr += '  <center>\n'
    optionsStr += '  <a href="' + optionsActor + '">\n'
    optionsStr += '  <img loading="lazy" src="' + optionsProfileUrl + \
        '" alt="" ' + getBrokenLinkSubstitute() + '/></a>\n'
    handle = getNicknameFromActor(optionsActor) + '@' + optionsDomain
    handleShown = handle
    if lockedAccount:
        handleShown += '🔒'
    if movedTo:
        handleShown += ' ⌂'
    if dormant:
        handleShown += ' 💤'
    optionsStr += \
        '  <p class="optionsText">' + translate['Options for'] + \
        ' @' + handleShown + '</p>\n'
    if followsYou:
        optionsStr += \
            '  <p class="optionsText">' + translate['Follows you'] + '</p>\n'
    if movedTo:
        newNickname = getNicknameFromActor(movedTo)
        newDomain, newPort = getDomainFromActor(movedTo)
        if newNickname and newDomain:
            newHandle = newNickname + '@' + newDomain
            optionsStr += \
                '  <p class="optionsText">' + \
                translate['New account'] + \
                ': <a href="' + movedTo + '">@' + newHandle + '</a></p>\n'
    elif alsoKnownAs:
        otherAccountsHtml = \
            '  <p class="optionsText">' + \
            translate['Other accounts'] + ': '

        ctr = 0
        if isinstance(alsoKnownAs, list):
            for altActor in alsoKnownAs:
                if altActor == optionsActor:
                    continue
                if ctr > 0:
                    otherAccountsHtml += ' '
                ctr += 1
                altDomain, altPort = getDomainFromActor(altActor)
                otherAccountsHtml += \
                    '<a href="' + altActor + '">' + altDomain + '</a>'
        elif isinstance(alsoKnownAs, str):
            if alsoKnownAs != optionsActor:
                ctr += 1
                altDomain, altPort = getDomainFromActor(alsoKnownAs)
                otherAccountsHtml += \
                    '<a href="' + alsoKnownAs + '">' + altDomain + '</a>'
        otherAccountsHtml += '</p>\n'
        if ctr > 0:
            optionsStr += otherAccountsHtml
    if emailAddress:
        optionsStr += \
            '<p class="imText">' + translate['Email'] + \
            ': <a href="mailto:' + \
            emailAddress + '">' + removeHtml(emailAddress) + '</a></p>\n'
    if xmppAddress:
        optionsStr += \
            '<p class="imText">' + translate['XMPP'] + \
            ': <a href="xmpp:' + removeHtml(xmppAddress) + '">' + \
            xmppAddress + '</a></p>\n'
    if matrixAddress:
        optionsStr += \
            '<p class="imText">' + translate['Matrix'] + ': ' + \
            removeHtml(matrixAddress) + '</p>\n'
    if ssbAddress:
        optionsStr += \
            '<p class="imText">SSB: ' + removeHtml(ssbAddress) + '</p>\n'
    if blogAddress:
        optionsStr += \
            '<p class="imText">Blog: <a href="' + \
            removeHtml(blogAddress) + '">' + \
            removeHtml(blogAddress) + '</a></p>\n'
    if toxAddress:
        optionsStr += \
            '<p class="imText">Tox: ' + removeHtml(toxAddress) + '</p>\n'
    if briarAddress:
        if briarAddress.startswith('briar://'):
            optionsStr += \
                '<p class="imText">' + \
                removeHtml(briarAddress) + '</p>\n'
        else:
            optionsStr += \
                '<p class="imText">briar://' + \
                removeHtml(briarAddress) + '</p>\n'
    if jamiAddress:
        optionsStr += \
            '<p class="imText">Jami: ' + removeHtml(jamiAddress) + '</p>\n'
    if PGPfingerprint:
        optionsStr += '<p class="pgp">PGP: ' + \
            removeHtml(PGPfingerprint).replace('\n', '<br>') + '</p>\n'
    if PGPpubKey:
        optionsStr += '<p class="pgp">' + \
            removeHtml(PGPpubKey).replace('\n', '<br>') + '</p>\n'
    optionsStr += '  <form method="POST" action="' + \
        originPathStr + '/personoptions">\n'
    optionsStr += '    <input type="hidden" name="pageNumber" value="' + \
        str(pageNumber) + '">\n'
    optionsStr += '    <input type="hidden" name="actor" value="' + \
        optionsActor + '">\n'
    optionsStr += '    <input type="hidden" name="avatarUrl" value="' + \
        optionsProfileUrl + '">\n'
    if optionsNickname:
        handle = optionsNickname + '@' + optionsDomainFull
        petname = getPetName(baseDir, nickname, domain, handle)
        optionsStr += \
            '    ' + translate['Petname'] + ': \n' + \
            '    <input type="text" name="optionpetname" value="' + \
            petname + '">\n' \
            '    <button type="submit" class="buttonsmall" ' + \
            'name="submitPetname">' + \
            translate['Submit'] + '</button><br>\n'

    # checkbox for receiving calendar events
    if isFollowingActor(baseDir, nickname, domain, optionsActor):
        checkboxStr = \
            '    <input type="checkbox" ' + \
            'class="profilecheckbox" name="onCalendar" checked> ' + \
            translate['Receive calendar events from this account'] + \
            '\n    <button type="submit" class="buttonsmall" ' + \
            'name="submitOnCalendar">' + \
            translate['Submit'] + '</button><br>\n'
        if not receivingCalendarEvents(baseDir, nickname, domain,
                                       optionsNickname, optionsDomainFull):
            checkboxStr = checkboxStr.replace(' checked>', '>')
        optionsStr += checkboxStr

    # checkbox for permission to post to newswire
    newswirePostsPermitted = False
    if optionsDomainFull == domainFull:
        adminNickname = getConfigParam(baseDir, 'admin')
        if (nickname == adminNickname or
            (isModerator(baseDir, nickname) and
             not isModerator(baseDir, optionsNickname))):
            newswireBlockedFilename = \
                baseDir + '/accounts/' + \
                optionsNickname + '@' + optionsDomain + '/.nonewswire'
            checkboxStr = \
                '    <input type="checkbox" ' + \
                'class="profilecheckbox" name="postsToNews" checked> ' + \
                translate['Allow news posts'] + \
                '\n    <button type="submit" class="buttonsmall" ' + \
                'name="submitPostToNews">' + \
                translate['Submit'] + '</button><br>\n'
            if os.path.isfile(newswireBlockedFilename):
                checkboxStr = checkboxStr.replace(' checked>', '>')
            else:
                newswirePostsPermitted = True
            optionsStr += checkboxStr

    # whether blogs created by this account are moderated on the newswire
    if newswirePostsPermitted:
        moderatedFilename = \
            baseDir + '/accounts/' + \
            optionsNickname + '@' + optionsDomain + '/.newswiremoderated'
        checkboxStr = \
            '    <input type="checkbox" ' + \
            'class="profilecheckbox" name="modNewsPosts" checked> ' + \
            translate['News posts are moderated'] + \
            '\n    <button type="submit" class="buttonsmall" ' + \
            'name="submitModNewsPosts">' + \
            translate['Submit'] + '</button><br>\n'
        if not os.path.isfile(moderatedFilename):
            checkboxStr = checkboxStr.replace(' checked>', '>')
        optionsStr += checkboxStr

    optionsStr += optionsLinkStr
    backPath = '/'
    if nickname:
        backPath = '/users/' + nickname + '/' + defaultTimeline
        if 'moderation' in backToPath:
            backPath = '/users/' + nickname + '/moderation'
    optionsStr += \
        '    <a href="' + backPath + '"><button type="button" ' + \
        'class="buttonIcon" name="submitBack">' + translate['Go Back'] + \
        '</button></a>\n'
    optionsStr += \
        '    <button type="submit" class="button" name="submitView">' + \
        translate['View'] + '</button>\n'
    optionsStr += donateStr
    optionsStr += \
        '    <button type="submit" class="button" name="submit' + \
        followStr + '">' + translate[followStr] + '</button>\n'
    optionsStr += \
        '    <button type="submit" class="button" name="submit' + \
        blockStr + '">' + translate[blockStr] + '</button>\n'
    optionsStr += \
        '    <button type="submit" class="button" name="submitDM">' + \
        translate['DM'] + '</button>\n'
    optionsStr += \
        '    <button type="submit" class="button" name="submit' + \
        snoozeButtonStr + '">' + translate[snoozeButtonStr] + '</button>\n'
    optionsStr += \
        '    <button type="submit" class="button" name="submitReport">' + \
        translate['Report'] + '</button>\n'

    if isModerator(baseDir, nickname):
        optionsStr += \
            '    <button type="submit" class="button" ' + \
            'name="submitPersonInfo">' + \
            translate['Info'] + '</button>\n'

    personNotes = ''
    personNotesFilename = \
        baseDir + '/accounts/' + nickname + '@' + domain + \
        '/notes/' + handle + '.txt'
    if os.path.isfile(personNotesFilename):
        with open(personNotesFilename, 'r') as fp:
            personNotes = fp.read()

    optionsStr += \
        '    <br><br>' + translate['Notes'] + ': \n'
    optionsStr += '    <button type="submit" class="buttonsmall" ' + \
        'name="submitPersonNotes">' + \
        translate['Submit'] + '</button><br>\n'
    optionsStr += \
        '    <textarea id="message" ' + \
        'name="optionnotes" style="height:400px">' + \
        personNotes + '</textarea>\n'

    optionsStr += '  </form>\n'
    optionsStr += '</center>\n'
    optionsStr += '</div>\n'
    optionsStr += '</div>\n'
    optionsStr += htmlFooter()
    return optionsStr
