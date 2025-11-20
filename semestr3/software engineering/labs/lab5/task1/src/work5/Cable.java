package work5;

/**
 * Елемент мережі, що представляє мережевий кабель.
 * Містить базові характеристики кабелю (довжина, ціна за метр)
 * та реалізує інтерфейс {@link NetworkElement} для роботи
 * з шаблоном {@code Visitor}.
 */
public class Cable implements NetworkElement {

    /**
     * Назва кабелю.
     */
    private final String name;

    /**
     * Довжина кабелю в метрах.
     */
    private final double lengthMeters;

    /**
     * Ціна за один метр кабелю.
     */
    private final double pricePerMeter;

    /**
     * Створює екземпляр кабелю з вказаними параметрами.
     * @param name          назва кабелю
     * @param lengthMeters  довжина в метрах
     * @param pricePerMeter ціна за метр
     */
    public Cable(String name, double lengthMeters, double pricePerMeter) {
        this.name = name;
        this.lengthMeters = lengthMeters;
        this.pricePerMeter = pricePerMeter;
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public String getName() {
        return name;
    }

    /**
     * Повертає довжину кабелю.
     * @return довжина в метрах
     */
    public double getLengthMeters() {
        return lengthMeters;
    }

    /**
     * Повертає ціну за метр кабелю.
     * @return ціна за метр
     */
    public double getPricePerMeter() {
        return pricePerMeter;
    }

    /**
     * Обчислює повну вартість кабелю як
     * {@code lengthMeters * pricePerMeter}.
     * @return повна вартість кабелю
     */
    public double getCost() {
        return lengthMeters * pricePerMeter;
    }

    /**
     * Приклад бізнес-методу із заглушкою.
     * У реальному застосунку тут могла б виконуватися
     * перевірка якості чи тестування кабелю. В цій
     * реалізації метод лише виводить інформаційне
     * повідомлення в консоль.
     */
    public void testCable() {
        System.out.println("Method testCable() called for cable '" + name + "'");
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void accept(NetworkVisitor visitor) {
        visitor.visitCable(this);
    }
}