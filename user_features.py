# feature to /pace button
def interval_charts(pace: int) -> str:
    """
    Takes pace in sec per 1km.
    Return interval distance charts by txt lines.
    """

    def to_time(sec: int) -> str:
        if sec > 60:
            minutes = int(sec / 60)
            seconds = sec - (minutes * 60)
            minutes = str(minutes)
            seconds = '0' + str(seconds) if seconds < 10 else str(seconds)
            return f'{minutes}:{seconds} мин.'
        else:
            return f'{sec} сек.'

    pace100m = round(pace * 0.1, 2)
    pace200m = to_time(round(pace * 0.2))
    pace400m = to_time(round(pace * 0.4))
    pace600m = to_time(round(pace * 0.6))
    pace800m = to_time(round(pace * 0.8))
    pace1200m = to_time(round(pace * 1.2))
    pace1km = to_time(pace)
    pace1600m = to_time(round(pace * 1.6))
    pace2km = to_time(pace * 2)
    pace3km = to_time(pace * 3)
    interval_workout = f'Раскладка на интервальную тренировку: \n\n' \
                       f'100м: {pace100m} сек.\n' \
                       f'200м: {pace200m} \n' \
                       f'400м: {pace400m} \n' \
                       f'600м: {pace600m} \n' \
                       f'800м: {pace800m} \n' \
                       f'1км: {pace1km} \n' \
                       f'1200м: {pace1200m} \n' \
                       f'1600м: {pace1600m} \n' \
                       f'2км: {pace2km} \n' \
                       f'3км: {pace3km}\n\n' \
                       f't.me/my_pace_bot'
    return interval_workout


# feature to /long button
def long_charts(pace: int) -> str:
    """
    Takes pace in sec per 1km.
    Return long distance charts by txt lines.
    """

    def to_time(sec: int) -> str:
        if sec > 3600:
            hours = int(sec / 3600)
            minutes = int((sec - hours * 3600) / 60)
            seconds = sec - hours * 3600 - minutes * 60
            minutes = '0' + str(minutes) if minutes < 10 else str(minutes)
            seconds = '0' + str(seconds) if seconds < 10 else str(seconds)
            return f'{hours}:{minutes}:{seconds} час.'
        else:
            minutes = int(sec / 60)
            seconds = sec - minutes * 60
            seconds = '0' + str(seconds) if seconds < 10 else str(seconds)
            return f'{minutes}:{seconds} мин.'

    pace1km = to_time(pace)
    pace2km = to_time(pace * 2)
    pace3km = to_time(pace * 3)
    pace4km = to_time(pace * 4)
    pace5km = to_time(pace * 5)
    pace6km = to_time(pace * 6)
    pace7km = to_time(pace * 7)
    pace8km = to_time(pace * 8)
    pace9km = to_time(pace * 9)
    pace10km = to_time(pace * 10)
    pace15km = to_time(pace * 15)
    pace20km = to_time(pace * 20)
    pace25km = to_time(pace * 25)
    pace30km = to_time(pace * 30)
    long_workout = f'Раскладка на длительную тренировку: \n\n' \
                       f'1км: {pace1km} \n' \
                       f'2км: {pace2km} \n' \
                       f'3км: {pace3km} \n' \
                       f'4км: {pace4km} \n' \
                       f'5км: {pace5km} \n' \
                       f'6км: {pace6km} \n' \
                       f'7км: {pace7km} \n' \
                       f'8км: {pace8km} \n' \
                       f'9км: {pace9km} \n' \
                       f'10км: {pace10km} \n' \
                       f'15км: {pace15km} \n' \
                       f'20км: {pace20km} \n' \
                       f'25км: {pace25km} \n' \
                       f'30км: {pace30km} \n\n' \
                       f't.me/my_pace_bot'
    return long_workout
