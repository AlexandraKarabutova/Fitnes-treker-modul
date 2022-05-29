from typing import Dict, Type, ClassVar
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message = ('Тип тренировки: {}; '
                   'Длительность: {:.3f} ч.; '
                   'Дистанция: {:.3f} км; '
                   'Ср. скорость: {:.3f} км/ч; '
                   'Потрачено ккал: {:.3f}.')
        return message.format(*asdict(self).values())


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60
    LEN_STEP: ClassVar[float] = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * Training.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> None:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите run в %s.'
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


@dataclass
class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        K_CAL_1: int = 18
        K_CAL_2: int = 20
        speed = self.get_mean_speed()
        dur_m = self.duration * Training.MIN_IN_HOUR
        calories = (K_CAL_1 * speed
                    - K_CAL_2) * self.weight / Training.M_IN_KM * dur_m
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: int

    def get_spent_calories(self) -> float:
        K_CAL_1: float = 0.035
        K_CAL_2: float = 0.029
        speed = self.get_mean_speed()
        duration_min = self.duration * Training.MIN_IN_HOUR
        calories = (K_CAL_1 * self.weight + (speed**2 // self.height)
                    * K_CAL_2 * self.weight) * duration_min
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: int
    count_pool: int
    LEN_STEP: ClassVar[float] = 1.38

    def get_distance(self) -> float:
        distance = self.action * Swimming.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        distance_pool_m = self.length_pool * self.count_pool / Training.M_IN_KM
        speed = distance_pool_m / self.duration
        return speed

    def get_spent_calories(self) -> float:
        K_CAL_1: float = 1.1
        K_CAL_2: int = 2
        speed = self.get_mean_speed()
        calories = (speed + K_CAL_1) * K_CAL_2 * self.weight
        return calories


def read_package(training_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if training_type in workout_types:
        return workout_types[training_type](*data)
    else:
        raise ValueError("Такой вид тренировки не найден.")


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
