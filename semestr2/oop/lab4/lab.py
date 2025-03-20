class Plane:

    # Клас для представлення літака з основними характеристиками

    def __init__(self, model: str, max_speed: int, flight_range: int, load_factor: float, passengers: int) -> None:

        """
        Ініціалізує літак із заданими характеристиками

        Аргументи:

            model (str): Назва моделі літака
            max_speed (int): Максимальна швидкість літака в км/год
            flight_range (int): Дальність польоту літака в км
            load_factor (int): Ванта літака в кг
            passengers (int): Кількість пасажирів на літаку

        return: None
        """

        self.model = model
        self.max_speed = max_speed
        self.flight_range = flight_range
        self.load_factor = load_factor
        self.passengers = passengers

    def __str__(self) -> str:

        """
        return: Рядок з відомостями про дані екземпляру класу
        """

        return f"Модель: {self.model}, Максимальна швидкість: {self.max_speed} км/год, Дальність польоту: {self.flight_range} км, Ванта: {self.load_factor} кг, passengers: {self.passengers}"
 
class Main:

    def __init__(self) -> None:

        """
        Ініціалізує список літаків
        """

        self.planes = []

    def initialize_planes(self) -> None:

        """
        Створює екземпляри класів Plane з переданими параметрами і додає їх до списку planes

        return: None
        """

        self.planes.append(Plane(model="Boeing 747", max_speed=988, flight_range=14815, load_factor=183500, passengers=660))
        self.planes.append(Plane(model="Airbus A320", max_speed=871, flight_range=6150, load_factor=73500, passengers=180))
        self.planes.append(Plane(model="Sukhoi Superjet 100", max_speed=870, flight_range=4500, load_factor=12250, passengers=108))
        self.planes.append(Plane(model="Concorde", max_speed=2179, flight_range=7222, load_factor=11970, passengers=128))
        self.planes.append(Plane(model="Cessna 172", max_speed=226, flight_range=1289, load_factor=400, passengers=4))

    def sorting_models(self) -> None:

        """
        Сортує список літаків за певною їх характеристикою

        return: None
        """

        print("Сортування літаів за алфавітним порядком їх моделей:\n")

        self.planes.sort(key=lambda plane: plane.model) # Використовуємо lambda для отримання доступу до змінної plane.model
        for plane in self.planes: print(plane)

        print("\nСортування літаків за максимальною швидкістю:\n")

        self.planes.sort(key=lambda plane: plane.max_speed, reverse=True) # reverse=True для спадаючого порядку
        for plane in self.planes: print(plane)

examples = Main()
examples.initialize_planes()
examples.sorting_models()