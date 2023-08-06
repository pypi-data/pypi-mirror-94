__filename__ = "filters.py"
__author__ = "Bob Mottram"
__license__ = "AGPL3+"
__version__ = "1.2.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@freedombone.net"
__status__ = "Production"

import os


def addFilter(baseDir: str, nickname: str, domain: str, words: str) -> bool:
    """Adds a filter for particular words within the content of a incoming posts
    """
    filtersFilename = baseDir + '/accounts/' + \
        nickname + '@' + domain + '/filters.txt'
    if os.path.isfile(filtersFilename):
        if words in open(filtersFilename).read():
            return False
    filtersFile = open(filtersFilename, "a+")
    filtersFile.write(words + '\n')
    filtersFile.close()
    return True


def addGlobalFilter(baseDir: str, words: str) -> bool:
    """Adds a global filter for particular words within
    the content of a incoming posts
    """
    if not words:
        return False
    if len(words) < 2:
        return False
    filtersFilename = baseDir + '/accounts/filters.txt'
    if os.path.isfile(filtersFilename):
        if words in open(filtersFilename).read():
            return False
    filtersFile = open(filtersFilename, "a+")
    filtersFile.write(words + '\n')
    filtersFile.close()
    return True


def removeFilter(baseDir: str, nickname: str, domain: str,
                 words: str) -> bool:
    """Removes a word filter
    """
    filtersFilename = baseDir + '/accounts/' + \
        nickname + '@' + domain + '/filters.txt'
    if os.path.isfile(filtersFilename):
        if words in open(filtersFilename).read():
            with open(filtersFilename, 'r') as fp:
                with open(filtersFilename + '.new', 'w+') as fpnew:
                    for line in fp:
                        line = line.replace('\n', '')
                        if line != words:
                            fpnew.write(line + '\n')
            if os.path.isfile(filtersFilename + '.new'):
                os.rename(filtersFilename + '.new', filtersFilename)
                return True
    return False


def removeGlobalFilter(baseDir: str, words: str) -> bool:
    """Removes a global word filter
    """
    filtersFilename = baseDir + '/accounts/filters.txt'
    if os.path.isfile(filtersFilename):
        if words in open(filtersFilename).read():
            with open(filtersFilename, 'r') as fp:
                with open(filtersFilename + '.new', 'w+') as fpnew:
                    for line in fp:
                        line = line.replace('\n', '')
                        if line != words:
                            fpnew.write(line + '\n')
            if os.path.isfile(filtersFilename + '.new'):
                os.rename(filtersFilename + '.new', filtersFilename)
                return True
    return False


def _isTwitterPost(content: str) -> bool:
    """Returns true if the given post content is a retweet or twitter crosspost
    """
    if '/twitter.' in content or '@twitter.' in content:
        return True
    elif '>RT <' in content:
        return True
    return False


def _isFilteredBase(filename: str, content: str) -> bool:
    """Uses the given file containing filtered words to check
    the given content
    """
    if not os.path.isfile(filename):
        return False

    with open(filename, 'r') as fp:
        for line in fp:
            filterStr = line.replace('\n', '').replace('\r', '')
            if not filterStr:
                continue
            if len(filterStr) < 2:
                continue
            if '+' not in filterStr:
                if filterStr in content:
                    return True
            else:
                filterWords = filterStr.replace('"', '').split('+')
                for word in filterWords:
                    if word not in content:
                        return False
                return True
    return False


def isFiltered(baseDir: str, nickname: str, domain: str, content: str) -> bool:
    """Should the given content be filtered out?
    This is a simple type of filter which just matches words, not a regex
    You can add individual words or use word1+word2 to indicate that two
    words must be present although not necessarily adjacent
    """
    globalFiltersFilename = baseDir + '/accounts/filters.txt'
    if _isFilteredBase(globalFiltersFilename, content):
        return True

    if not nickname or not domain:
        return False

    # optionally remove retweets
    removeTwitter = baseDir + '/accounts/' + \
        nickname + '@' + domain + '/.removeTwitter'
    if os.path.isfile(removeTwitter):
        if _isTwitterPost(content):
            return True

    accountFiltersFilename = baseDir + '/accounts/' + \
        nickname + '@' + domain + '/filters.txt'
    return _isFilteredBase(accountFiltersFilename, content)
