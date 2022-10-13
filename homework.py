from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Type


@dataclass
class InfoMessage:
    """Класс формирует информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
# Привет! Приятно познакомиться:) У меня возник вопрос,
# на который я не нашла ответ.
# Так и не дошло, почему пришлось убрать __init__.
# Есть идея, что это из-за asdict,
# так как он использует указатель на экземпляр.

    MESSAGE: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Метод возвращает строку сообщения."""

        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError

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

    COEFF_CALORIES_1: ClassVar[int] = 18
    COEFF_CALORIES_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEFF_CALORIES_1 * self.get_mean_speed()
                 - self.COEFF_CALORIES_2) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIES_1: ClassVar[float] = 0.035
    COEFF_CALORIES_2: ClassVar[int] = 2
    COEFF_CALORIES_3: ClassVar[float] = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEFF_CALORIES_1 * self.weight
                + (self.get_mean_speed() ** self.COEFF_CALORIES_2
                   // self.height)
                * self.COEFF_CALORIES_3 * self.weight)
                * self.MIN_IN_HOUR * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38
    COEFF_CALORIES_1: ClassVar[float] = 1.1
    COEFF_CALORIES_2: ClassVar[int] = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed() + self.COEFF_CALORIES_1)
                * self.COEFF_CALORIES_2 * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in workout:
        raise KeyError(f'Тренировка {workout_type} не найдена')
    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
# Вопросик и тут возник. Если изменить аннотацию
# на Type[Training] это повлечет изменения в коде ниже.
# Будет необходим указатель на экземпляр.

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
