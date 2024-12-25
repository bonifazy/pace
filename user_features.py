class Chart:
    def __init__(self, pace: int = 0, total_time: int = 0, distance: int = 0):
        """
        Takes pace in sec per 1km.
        """
        self.__time = total_time
        self.__distance = distance
        self.__pace = round(self.__time / self.__distance * 1000) if self.__time != 0 and self.__distance != 0 else pace
        self.correct_pace = True if 129 < self.__pace < 600 else False

    # feature to /pace button
    @property
    def interval(self) -> str:
        """
        Returns interval distance charts by txt lines.
        """
        interval_workout = f'Раскладка на интервальную тренировку,\nтемп: {self._target_time(1)}/ км: \n\n' \
                           f'100м: {round(self.__pace * 0.1, 2)} сек\n'
        for distance in [200, 400, 600, 800, 1000, 1200, 1600, 2000, 3000]:
            interval_workout += f'{distance}м: {self._target_time(distance * 0.001)} \n'
        return interval_workout + '\nt.me/my_pace_bot'

    # feature to /tempo button
    @property
    def tempo(self) -> str:
        """
        Returns tempo distance charts by txt lines.
        """
        tempo_workout = f'Раскладка на темповую тренировку,\nтемп: {self._target_time(1)}/ км: \n\n'
        for distance in range(1, 16):
            tempo_workout += f'{distance}км: {self._target_time(distance)} \n'
        return tempo_workout + '\nt.me/my_pace_bot'

    # feature to /long button
    @property
    def long(self) -> str:
        """
        Returns long distance charts by txt lines.
        """
        long_workout = f'Раскладка на длительную тренировку,\nтемп: {self._target_time(1)}/ км: \n\n'
        for distance in [5, 10, 15, 20, 25, 30]:
            long_workout += f'{distance}км: {self._target_time(distance)} \n'
        return long_workout + '\nt.me/my_pace_bot'

    # feature to /competitions button
    def competitions(self, distance_km) -> str:
        """
        Returns competitions distance charts by txt lines.
        """
        starts_charts = f'Раскладка на соревнования,\nтемп: {self._target_time(1)}/ км: \n\n'
        if distance_km == 3:
            for distance in [200, 400, 800, 1000, 1200, 1600, 2000, 2400, 2800, 3000]:
                starts_charts += f'{distance}м: {self._target_time(distance * 0.001)} \n'
        elif distance_km == 5:
            for distance in [200, 400, 800, 1000, 2000, 2500, 3000, 4000, 5000]:
                starts_charts += f'{distance}м: {self._target_time(distance * 0.001)} \n'
        elif distance_km == 10:
            for distance in [0.2, 0.4, 0.8, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                if distance < 1:
                    starts_charts += f'{int(distance * 1000)}м: {self._target_time(distance)} \n'
                else:
                    starts_charts += f'{distance}км: {self._target_time(distance)} \n'
        elif distance_km == 21:
            for distance in [5, 10, 10.55, 15, 20, 21.1]:
                if distance == 10.55:
                    starts_charts += f'{distance}0м: {self._target_time(distance)} (середина) \n'
                else:
                    starts_charts += f'{distance}км: {self._target_time(distance)} \n'
        elif distance_km == 42:
            for distance in [5, 10, 15, 20, 21.1, 25, 30, 35, 40, 42.2]:
                starts_charts += f'{distance}км: {self._target_time(distance)} \n'

        return starts_charts + '\nt.me/my_pace_bot'

    def laps_and_pace(self):
        """
        Returns distance charts and convert time to pace min/ km.
        """

        if not self.correct_pace:
            return None

        result = 'Раскладка, основные отрезки: \n'

        if self.__distance == 400:
            result += f'100м: {round(self.__pace * 0.1, 2)} сек\n'
            for lap in (2, 3, 4):
                result += f'{lap * 100} м: {self._target_time(lap * 0.1)} \n'
        elif self.__distance == 500:
            result += f'100м: {round(self.__pace * 0.1, 2)} сек\n'
            for lap in (2, 3, 4, 5):
                result += f'{lap * 100} м: {self._target_time(lap * 0.1)} \n'
        elif self.__distance == 600:
            result += f'100м: {round(self.__pace * 0.1, 2)} сек\n'
            for lap in (2, 3, 4, 5, 6):
                result += f'{lap * 100} м: {self._target_time(lap * 0.1)} \n'
        elif self.__distance == 800:
            result += f'100м: {round(self.__pace * 0.1, 2)} сек\n'
            for lap in (2, 4, 6, 8):
                result += f'{lap * 100} м: {self._target_time(lap * 0.1)} \n'
        elif self.__distance == 1000:
            result += f'100м: {round(self.__pace * 0.1, 2)} сек\n'
            for lap in (2, 4, 5, 8, 10):
                result += f'{lap * 100} м: {self._target_time(lap * 0.1)} \n'
        elif self.__distance == 1200:
            for lap in (2, 4, 6, 8, 10, 12):
                result += f'{lap * 100} м: {self._target_time(lap * 0.1)} \n'
        if self.__distance == 1500:
            for lap in (4, 5, 8, 10, 12, 15):
                result += f'{lap * 100} м: {self._target_time(lap * 0.1)} \n'
        if self.__distance == 1600:
            for lap in (4, 8, 12, 16):
                result += f'{lap * 100} м: {self._target_time(lap * 0.1)} \n'
        if self.__distance == 2000:
            for lap in (4, 8, 10, 12, 16, 20):
                result += f'{lap * 100} м: {self._target_time(lap * 0.1)} \n'
        if self.__distance == 3000:
            for lap in (4, 8, 10, 12, 15, 16, 20, 24, 30):
                result += f'{lap * 100} м: {self._target_time(lap * 0.1)} \n'
        if self.__distance == 4000:
            for lap in (4, 8, 10, 15, 20, 25, 30, 35, 40):
                result += f'{lap * 100} м: {self._target_time(lap * 0.1)} \n'
        if self.__distance == 5000:
            for lap in (4, 8, 10, 15, 20, 25, 30, 35, 40, 45, 50):
                result += f'{lap * 100} м: {self._target_time(lap * 0.1)} \n'
        result += f'\nТемп: {self._target_time()}/ км.'

        return result + '\nt.me/my_pace_bot'

    @staticmethod
    def _to_time(sec: int) -> str:
        if sec >= 3600:
            hours = sec // 3600
            return f'{hours}:{(sec - hours * 3600) // 60:02d}:{sec % 60:02d} час'
        elif sec > 60:
            return f'{sec // 60}:{sec % 60:02d} мин'
        else:
            return f'{sec} сек'

    def _target_time(self, distance: float = 1.0) -> str:
        """
        distance: Distance in km

        returns: total time in seconds
        """
        return self._to_time(round(self.__pace * distance))
