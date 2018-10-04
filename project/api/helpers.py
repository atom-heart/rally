from datetime import datetime, timedelta

from project.filters import timefilter


def add_positions(ranking):
    """Determines player positions. Assumes input list of players is sorted"""
    prev = None

    for pos, player in enumerate(ranking, start=1):
        # First is always first
        if pos is 1 and (player['time'] or player['disqualified']):
            player['position'] = pos

        # Same position for players with same time
        elif player['time'] and player['time'] == prev['time']:
            player['position'] = prev['position']

        # Same position for all disqualified
        elif player['disqualified'] and prev['disqualified']:
            player['position'] = prev['position']

        # Base case
        elif player['time'] or player['disqualified']:
            player['position'] = pos

        else:
            break

        prev = player

    return ranking


def add_stage_positions(ranking):
    prev = None

    for pos, player in enumerate(ranking, start=1):
        if pos is 1:
            player['position'] = pos

        elif player['points'] == prev['points']:
            player['position'] = prev['position']

        else:
            player['position'] = pos

        prev = player

    return ranking


def add_pos_diffs(prev, curr):
    """Determines position differences betwen current and previous split progresses"""
    prev_pos = {player['id']: player['position'] for player in prev}

    for player in curr:
        id = player['id']
        player['position_diff'] = prev_pos[id] - player['position']

    return curr


def add_time_diffs(ranking):
    """Determines time differences"""
    first = ranking[0]

    for player in ranking:
        if player['time'] and player is not first:
            player['time_diff'] = player['time'] - first['time']
        else:
            player['time_diff'] = None
        prev = player

    return ranking


def format_times_diffs(ranking):
    """Formats times and time differences"""
    for player in ranking:
        player['time'] = timefilter(player['time'])
        player['time_diff'] = timefilter(player['time_diff'])

    return ranking


def group_players(players):
    """
    Divides players into groups: `finished`, `disqualified` and, optionally, `not_finished`.

    args:
        players: dict of players, with their ID as the key, containing (among others)
            `disqualified` (bool) property

    returns:
        grouped: dict of lists (groups) of players
    """
    grouped = {'finished': [], 'disqualified': [], 'not_finished': []}

    for player in players:
        # Save `disqualified` property to temporary variable, and delete from player dict
        disq = player['disqualified']
        del player['disqualified']

        # Assign to suitable groups
        if disq:
            grouped['disqualified'].append(player)
        elif player['time']:
            grouped['finished'].append(player)
        else:
            grouped['not_finished'].append(player)

    return grouped


def group_players_ranking(players):
    """
    Divides players into groups: `finished`, `disqualified` and, optionally, `not_finished`.

    args:
        players: dict of players, with their ID as the key, containing (among others)
            `disqualified` (bool) property

    returns:
        grouped: dict of lists (groups) of players
    """
    grouped = {'finished': [], 'disqualified': [], 'not_finished': [], 'stage_disqualified': []}

    for player in players:
        # Save `disqualified` property to temporary variable, and delete from player dict
        disq = player['disqualified']
        stage_disq = player['stage_disqualified']
        del player['disqualified']
        del player['stage_disqualified']

        # Assign to suitable groups
        if player['time']:
            grouped['finished'].append(player)
        elif disq:
            grouped['disqualified'].append(player)
        elif stage_disq:
            grouped['stage_disqualified'].append(player)
        else:
            grouped['not_finished'].append(player)

    return grouped


def normalize(keys, players):
    return [dict(zip(keys, player)) for player in players]


def strToTimedelta(datestring):
    """Converts JavaScript datetime string to Python timedelta"""
    dt = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S.%fZ')
    td = timedelta(
        hours=dt.hour,
        minutes=dt.minute,
        seconds=dt.second,
        microseconds=dt.microsecond
    )

    return td


def assign_points(players):
    # temp point system which works only works for 4 or less players
    points = [5, 3, 1, 0]

    result = {}
    for player in players:
        result[player['id']] = 0 if player['disqualified'] else points[player['position'] - 1]

    return result
