__filename__ = "happening.py"
__author__ = "Bob Mottram"
__license__ = "AGPL3+"
__version__ = "1.2.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@freedombone.net"
__status__ = "Production"

import os
from uuid import UUID
from datetime import datetime

from utils import loadJson
from utils import saveJson
from utils import locatePost
from utils import daysInMonth
from utils import mergeDicts


def _validUuid(testUuid: str, version=4):
    """Check if uuid_to_test is a valid UUID
    """
    try:
        uuid_obj = UUID(testUuid, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == testUuid


def _removeEventFromTimeline(eventId: str, tlEventsFilename: str) -> None:
    """Removes the given event Id from the timeline
    """
    if eventId + '\n' not in open(tlEventsFilename).read():
        return
    with open(tlEventsFilename, 'r') as fp:
        eventsTimeline = fp.read().replace(eventId + '\n', '')
        try:
            with open(tlEventsFilename, 'w+') as fp2:
                fp2.write(eventsTimeline)
        except BaseException:
            print('ERROR: unable to save events timeline')
            pass


def saveEventPost(baseDir: str, handle: str, postId: str,
                  eventJson: {}) -> bool:
    """Saves an event to the calendar and/or the events timeline
    If an event has extra fields, as per Mobilizon,
    Then it is saved as a separate entity and added to the
    events timeline
    See https://framagit.org/framasoft/mobilizon/-/blob/
    master/lib/federation/activity_stream/converter/event.ex
    """
    calendarPath = baseDir + '/accounts/' + handle + '/calendar'
    if not os.path.isdir(calendarPath):
        os.mkdir(calendarPath)

    # get the year, month and day from the event
    eventTime = datetime.strptime(eventJson['startTime'],
                                  "%Y-%m-%dT%H:%M:%S%z")
    eventYear = int(eventTime.strftime("%Y"))
    if eventYear < 2020 or eventYear >= 2100:
        return False
    eventMonthNumber = int(eventTime.strftime("%m"))
    if eventMonthNumber < 1 or eventMonthNumber > 12:
        return False
    eventDayOfMonth = int(eventTime.strftime("%d"))
    if eventDayOfMonth < 1 or eventDayOfMonth > 31:
        return False

    if eventJson.get('name') and eventJson.get('actor') and \
       eventJson.get('uuid') and eventJson.get('content'):
        if not _validUuid(eventJson['uuid']):
            return False
        print('Mobilizon type event')
        # if this is a full description of an event then save it
        # as a separate json file
        eventsPath = baseDir + '/accounts/' + handle + '/events'
        if not os.path.isdir(eventsPath):
            os.mkdir(eventsPath)
        eventsYearPath = \
            baseDir + '/accounts/' + handle + '/events/' + str(eventYear)
        if not os.path.isdir(eventsYearPath):
            os.mkdir(eventsYearPath)
        eventId = str(eventYear) + '-' + eventTime.strftime("%m") + '-' + \
            eventTime.strftime("%d") + '_' + eventJson['uuid']
        eventFilename = eventsYearPath + '/' + eventId + '.json'

        saveJson(eventJson, eventFilename)
        # save to the events timeline
        tlEventsFilename = baseDir + '/accounts/' + handle + '/events.txt'

        if os.path.isfile(tlEventsFilename):
            _removeEventFromTimeline(eventId, tlEventsFilename)
            try:
                with open(tlEventsFilename, 'r+') as tlEventsFile:
                    content = tlEventsFile.read()
                    if eventId + '\n' not in content:
                        tlEventsFile.seek(0, 0)
                        tlEventsFile.write(eventId + '\n' + content)
            except Exception as e:
                print('WARN: Failed to write entry to events file ' +
                      tlEventsFilename + ' ' + str(e))
                return False
        else:
            tlEventsFile = open(tlEventsFilename, 'w+')
            tlEventsFile.write(eventId + '\n')
            tlEventsFile.close()

    # create a directory for the calendar year
    if not os.path.isdir(calendarPath + '/' + str(eventYear)):
        os.mkdir(calendarPath + '/' + str(eventYear))

    # calendar month file containing event post Ids
    calendarFilename = calendarPath + '/' + str(eventYear) + \
        '/' + str(eventMonthNumber) + '.txt'

    # Does this event post already exist within the calendar month?
    if os.path.isfile(calendarFilename):
        if postId in open(calendarFilename).read():
            # Event post already exists
            return False

    # append the post Id to the file for the calendar month
    calendarFile = open(calendarFilename, 'a+')
    if not calendarFile:
        return False
    calendarFile.write(postId + '\n')
    calendarFile.close()

    # create a file which will trigger a notification that
    # a new event has been added
    calendarNotificationFilename = \
        baseDir + '/accounts/' + handle + '/.newCalendar'
    calendarNotificationFile = \
        open(calendarNotificationFilename, 'w+')
    if not calendarNotificationFile:
        return False
    calendarNotificationFile.write('/calendar?year=' +
                                   str(eventYear) +
                                   '?month=' +
                                   str(eventMonthNumber) +
                                   '?day=' +
                                   str(eventDayOfMonth))
    calendarNotificationFile.close()
    return True


def _isHappeningEvent(tag: {}) -> bool:
    """Is this tag an Event or Place ActivityStreams type?
    """
    if not tag.get('type'):
        return False
    if tag['type'] != 'Event' and tag['type'] != 'Place':
        return False
    return True


def _isHappeningPost(postJsonObject: {}) -> bool:
    """Is this a post with tags?
    """
    if not postJsonObject:
        return False
    if not postJsonObject.get('object'):
        return False
    if not isinstance(postJsonObject['object'], dict):
        return False
    if not postJsonObject['object'].get('tag'):
        return False
    return True


def getTodaysEvents(baseDir: str, nickname: str, domain: str,
                    currYear=None, currMonthNumber=None,
                    currDayOfMonth=None) -> {}:
    """Retrieves calendar events for today
    Returns a dictionary of lists containing Event and Place activities
    """
    now = datetime.now()
    if not currYear:
        year = now.year
    else:
        year = currYear
    if not currMonthNumber:
        monthNumber = now.month
    else:
        monthNumber = currMonthNumber
    if not currDayOfMonth:
        dayNumber = now.day
    else:
        dayNumber = currDayOfMonth

    calendarFilename = \
        baseDir + '/accounts/' + nickname + '@' + domain + \
        '/calendar/' + str(year) + '/' + str(monthNumber) + '.txt'
    events = {}
    if not os.path.isfile(calendarFilename):
        return events

    calendarPostIds = []
    recreateEventsFile = False
    with open(calendarFilename, 'r') as eventsFile:
        for postId in eventsFile:
            postId = postId.replace('\n', '').replace('\r', '')
            postFilename = locatePost(baseDir, nickname, domain, postId)
            if not postFilename:
                recreateEventsFile = True
                continue

            postJsonObject = loadJson(postFilename)
            if not _isHappeningPost(postJsonObject):
                continue

            postEvent = []
            dayOfMonth = None
            for tag in postJsonObject['object']['tag']:
                if not _isHappeningEvent(tag):
                    continue
                # this tag is an event or a place
                if tag['type'] == 'Event':
                    # tag is an event
                    if not tag.get('startTime'):
                        continue
                    eventTime = \
                        datetime.strptime(tag['startTime'],
                                          "%Y-%m-%dT%H:%M:%S%z")
                    if int(eventTime.strftime("%Y")) == year and \
                       int(eventTime.strftime("%m")) == monthNumber and \
                       int(eventTime.strftime("%d")) == dayNumber:
                        dayOfMonth = str(int(eventTime.strftime("%d")))
                        if '#statuses#' in postId:
                            # link to the id so that the event can be
                            # easily deleted
                            tag['postId'] = postId.split('#statuses#')[1]
                        postEvent.append(tag)
                else:
                    # tag is a place
                    postEvent.append(tag)
            if postEvent and dayOfMonth:
                calendarPostIds.append(postId)
                if not events.get(dayOfMonth):
                    events[dayOfMonth] = []
                events[dayOfMonth].append(postEvent)

    # if some posts have been deleted then regenerate the calendar file
    if recreateEventsFile:
        calendarFile = open(calendarFilename, 'w+')
        for postId in calendarPostIds:
            calendarFile.write(postId + '\n')
        calendarFile.close()

    return events


def todaysEventsCheck(baseDir: str, nickname: str, domain: str) -> bool:
    """Are there calendar events today?
    """
    now = datetime.now()
    year = now.year
    monthNumber = now.month
    dayNumber = now.day

    calendarFilename = \
        baseDir + '/accounts/' + nickname + '@' + domain + \
        '/calendar/' + str(year) + '/' + str(monthNumber) + '.txt'
    if not os.path.isfile(calendarFilename):
        return False

    eventsExist = False
    with open(calendarFilename, 'r') as eventsFile:
        for postId in eventsFile:
            postId = postId.replace('\n', '').replace('\r', '')
            postFilename = locatePost(baseDir, nickname, domain, postId)
            if not postFilename:
                continue

            postJsonObject = loadJson(postFilename)
            if not _isHappeningPost(postJsonObject):
                continue

            for tag in postJsonObject['object']['tag']:
                if not _isHappeningEvent(tag):
                    continue
                # this tag is an event or a place
                if tag['type'] != 'Event':
                    continue
                # tag is an event
                if not tag.get('startTime'):
                    continue
                eventTime = \
                    datetime.strptime(tag['startTime'],
                                      "%Y-%m-%dT%H:%M:%S%z")
                if int(eventTime.strftime("%Y")) == year and \
                   int(eventTime.strftime("%m")) == monthNumber and \
                   int(eventTime.strftime("%d")) == dayNumber:
                    eventsExist = True
                    break

    return eventsExist


def thisWeeksEventsCheck(baseDir: str, nickname: str, domain: str) -> bool:
    """Are there calendar events this week?
    """
    now = datetime.now()
    year = now.year
    monthNumber = now.month
    dayNumber = now.day

    calendarFilename = \
        baseDir + '/accounts/' + nickname + '@' + domain + \
        '/calendar/' + str(year) + '/' + str(monthNumber) + '.txt'
    if not os.path.isfile(calendarFilename):
        return False

    eventsExist = False
    with open(calendarFilename, 'r') as eventsFile:
        for postId in eventsFile:
            postId = postId.replace('\n', '').replace('\r', '')
            postFilename = locatePost(baseDir, nickname, domain, postId)
            if not postFilename:
                continue

            postJsonObject = loadJson(postFilename)
            if not _isHappeningPost(postJsonObject):
                continue

            for tag in postJsonObject['object']['tag']:
                if not _isHappeningEvent(tag):
                    continue
                # this tag is an event or a place
                if tag['type'] != 'Event':
                    continue
                # tag is an event
                if not tag.get('startTime'):
                    continue
                eventTime = \
                    datetime.strptime(tag['startTime'],
                                      "%Y-%m-%dT%H:%M:%S%z")
                if (int(eventTime.strftime("%Y")) == year and
                    int(eventTime.strftime("%m")) == monthNumber and
                    (int(eventTime.strftime("%d")) > dayNumber and
                     int(eventTime.strftime("%d")) <= dayNumber + 6)):
                    eventsExist = True
                    break

    return eventsExist


def getThisWeeksEvents(baseDir: str, nickname: str, domain: str) -> {}:
    """Retrieves calendar events for this week
    Returns a dictionary indexed by day number of lists containing
    Event and Place activities
    Note: currently not used but could be with a weekly calendar screen
    """
    now = datetime.now()
    year = now.year
    monthNumber = now.month
    dayNumber = now.day

    calendarFilename = \
        baseDir + '/accounts/' + nickname + '@' + domain + \
        '/calendar/' + str(year) + '/' + str(monthNumber) + '.txt'

    events = {}
    if not os.path.isfile(calendarFilename):
        return events

    calendarPostIds = []
    recreateEventsFile = False
    with open(calendarFilename, 'r') as eventsFile:
        for postId in eventsFile:
            postId = postId.replace('\n', '').replace('\r', '')
            postFilename = locatePost(baseDir, nickname, domain, postId)
            if not postFilename:
                recreateEventsFile = True
                continue

            postJsonObject = loadJson(postFilename)
            if not _isHappeningPost(postJsonObject):
                continue

            postEvent = []
            dayOfMonth = None
            weekDayIndex = None
            for tag in postJsonObject['object']['tag']:
                if not _isHappeningEvent(tag):
                    continue
                # this tag is an event or a place
                if tag['type'] == 'Event':
                    # tag is an event
                    if not tag.get('startTime'):
                        continue
                    eventTime = \
                        datetime.strptime(tag['startTime'],
                                          "%Y-%m-%dT%H:%M:%S%z")
                    if (int(eventTime.strftime("%Y")) == year and
                        int(eventTime.strftime("%m")) == monthNumber and
                        (int(eventTime.strftime("%d")) >= dayNumber and
                         int(eventTime.strftime("%d")) <= dayNumber + 6)):
                        dayOfMonth = str(int(eventTime.strftime("%d")))
                        weekDayIndex = dayOfMonth - dayNumber
                        postEvent.append(tag)
                else:
                    # tag is a place
                    postEvent.append(tag)
            if postEvent and weekDayIndex:
                calendarPostIds.append(postId)
                if not events.get(dayOfMonth):
                    events[weekDayIndex] = []
                events[dayOfMonth].append(postEvent)

    # if some posts have been deleted then regenerate the calendar file
    if recreateEventsFile:
        calendarFile = open(calendarFilename, 'w+')
        for postId in calendarPostIds:
            calendarFile.write(postId + '\n')
        calendarFile.close()

    lastDayOfMonth = daysInMonth(year, monthNumber)
    if dayNumber+6 > lastDayOfMonth:
        monthNumber += 1
        if monthNumber > 12:
            monthNumber = 1
            year += 1
        for d in range(1, dayNumber + 6 - lastDayOfMonth):
            dailyEvents = \
                getTodaysEvents(baseDir, nickname, domain,
                                year, monthNumber, d)
            if dailyEvents:
                if dailyEvents.get(d):
                    newEvents = {}
                    newEvents[d + (7 - (dayNumber + 6 - lastDayOfMonth))] = \
                        dailyEvents[d]
                    events = mergeDicts(events, newEvents)

    return events


def getCalendarEvents(baseDir: str, nickname: str, domain: str,
                      year: int, monthNumber: int) -> {}:
    """Retrieves calendar events
    Returns a dictionary indexed by day number of lists containing
    Event and Place activities
    """
    calendarFilename = \
        baseDir + '/accounts/' + nickname + '@' + domain + \
        '/calendar/' + str(year) + '/' + str(monthNumber) + '.txt'

    events = {}
    if not os.path.isfile(calendarFilename):
        return events

    calendarPostIds = []
    recreateEventsFile = False
    with open(calendarFilename, 'r') as eventsFile:
        for postId in eventsFile:
            postId = postId.replace('\n', '').replace('\r', '')
            postFilename = locatePost(baseDir, nickname, domain, postId)
            if not postFilename:
                recreateEventsFile = True
                continue

            postJsonObject = loadJson(postFilename)
            if not _isHappeningPost(postJsonObject):
                continue

            postEvent = []
            dayOfMonth = None
            for tag in postJsonObject['object']['tag']:
                if not _isHappeningEvent(tag):
                    continue
                # this tag is an event or a place
                if tag['type'] == 'Event':
                    # tag is an event
                    if not tag.get('startTime'):
                        continue
                    eventTime = \
                        datetime.strptime(tag['startTime'],
                                          "%Y-%m-%dT%H:%M:%S%z")
                    if int(eventTime.strftime("%Y")) == year and \
                       int(eventTime.strftime("%m")) == monthNumber:
                        dayOfMonth = str(int(eventTime.strftime("%d")))
                        postEvent.append(tag)
                else:
                    # tag is a place
                    postEvent.append(tag)

            if postEvent and dayOfMonth:
                calendarPostIds.append(postId)
                if not events.get(dayOfMonth):
                    events[dayOfMonth] = []
                events[dayOfMonth].append(postEvent)

    # if some posts have been deleted then regenerate the calendar file
    if recreateEventsFile:
        calendarFile = open(calendarFilename, 'w+')
        for postId in calendarPostIds:
            calendarFile.write(postId + '\n')
        calendarFile.close()

    return events


def removeCalendarEvent(baseDir: str, nickname: str, domain: str,
                        year: int, monthNumber: int, messageId: str) -> None:
    """Removes a calendar event
    """
    calendarFilename = \
        baseDir + '/accounts/' + nickname + '@' + domain + \
        '/calendar/' + str(year) + '/' + str(monthNumber) + '.txt'
    if not os.path.isfile(calendarFilename):
        return
    if '/' in messageId:
        messageId = messageId.replace('/', '#')
    if messageId not in open(calendarFilename).read():
        return
    lines = None
    with open(calendarFilename, "r") as f:
        lines = f.readlines()
    if not lines:
        return
    with open(calendarFilename, "w+") as f:
        for line in lines:
            if messageId not in line:
                f.write(line)
