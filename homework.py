
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    min_in_hour: int = 60
    LEN_STEP: float = 0.65

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * Training.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        k_cal_1: int = 18
        k_cal_2: int = 20
        speed = self.get_mean_speed()
        dur_m = self.duration * Training.min_in_hour
        calories = (k_cal_1 * speed
                    - k_cal_2) * self.weight / Training.M_IN_KM * dur_m
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        k_cal_1: float = 0.035
        k_cal_2: float = 0.029
        speed = self.get_mean_speed()
        duration_min = self.duration * Training.min_in_hour
        calories = (k_cal_1 * self.weight + (speed**2 // self.height)
                    * k_cal_2 * self.weight) * duration_min
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        distance = self.action * Swimming.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        distance_pool_m = self.length_pool * self.count_pool / Training.M_IN_KM
        speed = distance_pool_m / self.duration
        return speed

    def get_spent_calories(self) -> float:
        k_cal_1: float = 1.1
        k_cal_2: int = 2
        speed = self.get_mean_speed()
        calories = (speed + k_cal_1) * k_cal_2 * self.weight
        return calories


def read_package(training_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return dict_training[training_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for training_type, data in packages:
        training = read_package(training_type, data)
        main(training)
