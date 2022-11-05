class Chart:
    def __init__(self, pace: int) -> None:
        """
        Takes pace in sec per 1km.
        """
        self.__pace = pace

    # feature to /pace button
    @property
    def interval(self) -> str:
        """
        Returns interval distance charts by txt lines.
        """
        interval_workout = f'Темп: {self._target_time(1)} мин/ км. \n\n' \
                           f'Раскладка на интервальную тренировку: \n\n' \
                           f'100м: {round(self.__pace * 0.1, 2)} сек.\n'
        for distance in [200, 400, 600, 800, 1000, 1200, 1600, 2000, 3000]:
            interval_workout += f'{distance}м: {self._target_time(distance / 1000)} \n'
        return interval_workout + '\nt.me/my_pace_bot'

    # feature to /tempo button
    @property
    def tempo(self) -> str:
        """
        Returns tempo distance charts by txt lines.
        """
        tempo_workout = f'Темп: {self._target_time(1)} мин/ км. \n\n' \
                        f'Раскладка на темповую тренировку: \n\n'
        for distance in range(1, 16):
            tempo_workout += f'{distance}км: {self._target_time(distance)} \n'
        return tempo_workout + '\nt.me/my_pace_bot'

    # feature to /long button
    @property
    def long(self) -> str:
        """
        Returns long distance charts by txt lines.
        """
        long_workout = f'Темп: {self._target_time(1)} мин/ км. \n\nРаскладка на длительную тренировку: \n\n'
        for distance in [5, 10, 15, 20, 25, 30]:
            long_workout += f'{distance}км: {self._target_time(distance)} \n'
        return long_workout + '\nt.me/my_pace_bot'

    @staticmethod
    def _to_time(sec: int) -> str:
        if sec > 3600:
            hours = sec // 3600
            return f'{hours}:{(sec - hours * 3600) // 60:02d}:{sec % 60:02d} час.'
        elif sec > 60:
            return f'{sec // 60}:{sec % 60:02d} мин.'
        else:
            return f'{sec} сек.'

    def _target_time(self, distance: float) -> str:
        """
        distance: Distance in km
        """
        return self._to_time(round(self.__pace * distance))
