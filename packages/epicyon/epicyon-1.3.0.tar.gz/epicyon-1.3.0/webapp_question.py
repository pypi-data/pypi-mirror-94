__filename__ = "webapp_question.py"
__author__ = "Bob Mottram"
__license__ = "AGPL3+"
__version__ = "1.2.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@freedombone.net"
__status__ = "Production"

import os
from question import isQuestion
from utils import removeIdEnding


def insertQuestion(baseDir: str, translate: {},
                   nickname: str, domain: str, port: int,
                   content: str,
                   postJsonObject: {}, pageNumber: int) -> str:
    """ Inserts question selection into a post
    """
    if not isQuestion(postJsonObject):
        return content
    if len(postJsonObject['object']['oneOf']) == 0:
        return content
    messageId = removeIdEnding(postJsonObject['id'])
    if '#' in messageId:
        messageId = messageId.split('#', 1)[0]
    pageNumberStr = ''
    if pageNumber:
        pageNumberStr = '?page=' + str(pageNumber)

    votesFilename = \
        baseDir + '/accounts/' + nickname + '@' + domain + '/questions.txt'

    showQuestionResults = False
    if os.path.isfile(votesFilename):
        if messageId in open(votesFilename).read():
            showQuestionResults = True

    if not showQuestionResults:
        # show the question options
        content += '<div class="question">'
        content += \
            '<form method="POST" action="/users/' + \
            nickname + '/question' + pageNumberStr + '">\n'
        content += \
            '<input type="hidden" name="messageId" value="' + \
            messageId + '">\n<br>\n'
        for choice in postJsonObject['object']['oneOf']:
            if not choice.get('type'):
                continue
            if not choice.get('name'):
                continue
            content += \
                '<input type="radio" name="answer" value="' + \
                choice['name'] + '"> ' + choice['name'] + '<br><br>\n'
        content += \
            '<input type="submit" value="' + \
            translate['Vote'] + '" class="vote"><br><br>\n'
        content += '</form>\n</div>\n'
    else:
        # show the responses to a question
        content += '<div class="questionresult">\n'

        # get the maximum number of votes
        maxVotes = 1
        for questionOption in postJsonObject['object']['oneOf']:
            if not questionOption.get('name'):
                continue
            if not questionOption.get('replies'):
                continue
            votes = 0
            try:
                votes = int(questionOption['replies']['totalItems'])
            except BaseException:
                pass
            if votes > maxVotes:
                maxVotes = int(votes+1)

        # show the votes as sliders
        questionCtr = 1
        for questionOption in postJsonObject['object']['oneOf']:
            if not questionOption.get('name'):
                continue
            if not questionOption.get('replies'):
                continue
            votes = 0
            try:
                votes = int(questionOption['replies']['totalItems'])
            except BaseException:
                pass
            votesPercent = str(int(votes * 100 / maxVotes))
            content += \
                '<p><input type="text" title="' + str(votes) + \
                '" name="skillName' + str(questionCtr) + \
                '" value="' + questionOption['name'] + \
                ' (' + str(votes) + ')" style="width:40%">\n'
            content += \
                '<input type="range" min="1" max="100" ' + \
                'class="slider" title="' + \
                str(votes) + '" name="skillValue' + str(questionCtr) + \
                '" value="' + votesPercent + '"></p>\n'
            questionCtr += 1
        content += '</div>\n'
    return content
