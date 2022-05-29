from typing import Dict, Type
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60
    LEN_STEP: float = 0.65

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> None:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите метод get_spent_calories в %s.'
                                  % (self.__class__.__name__))

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

    K_CAL_1: int = 18
    K_CAL_2: int = 20

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        dur_m = self.duration * self.MIN_IN_HOUR
        calories = (self.K_CAL_1 * speed
                    - self.K_CAL_2) * self.weight / self.M_IN_KM * dur_m
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    K_CAL_1: float = 0.035
    K_CAL_2: float = 0.029

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
        speed = self.get_mean_speed()
        duration_min = self.duration * self.MIN_IN_HOUR
        calories = (self.K_CAL_1 * self.weight + (speed**2 // self.height)
                    * self.K_CAL_2 * self.weight) * duration_min
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    K_CAL_1: float = 1.1
    K_CAL_2: int = 2

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        distance_pool_m = self.length_pool * self.count_pool / self.M_IN_KM
        speed = distance_pool_m / self.duration
        return speed

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        calories = (speed + self.K_CAL_1) * self.K_CAL_2 * self.weight
        return calories


def read_package(training_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if training_type not in workout_types:
        raise ValueError("Такой вид тренировки не найден.")
    return workout_types[training_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for training_type, data in packages:
        training = read_package(training_type, data)
        main(training)
