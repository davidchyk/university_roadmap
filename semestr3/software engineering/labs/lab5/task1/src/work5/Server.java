package work5;

/**
 * Елемент мережі, що представляє сервер.
 * Зберігає базову вартість сервера та кількість процесорних ядер.
 * Реалізує інтерфейс {@link NetworkElement} для підтримки шаблону
 * {@code Visitor}.
 */
public class Server implements NetworkElement {

    /**
     * Назва сервера.
     */
    private final String name;

    /**
     * Базова вартість сервера.
     */
    private final double baseCost;

    /**
     * Кількість процесорних ядер.
     */
    private final int cpuCores;

    /**
     * Створює новий сервер з указаними параметрами.
     * @param name     назва сервера
     * @param baseCost базова вартість
     * @param cpuCores кількість процесорних ядер
     */
    public Server(String name, double baseCost, int cpuCores) {
        this.name = name;
        this.baseCost = baseCost;
        this.cpuCores = cpuCores;
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public String getName() {
        return name;
    }

    /**
     * Повертає базову вартість сервера.
     * @return вартість сервера
     */
    public double getBaseCost() {
        return baseCost;
    }

    /**
     * Повертає кількість процесорних ядер.
     * @return кількість ядер
     */
    public int getCpuCores() {
        return cpuCores;
    }

    /**
     * Бізнес-метод із заглушкою.
     * Може символізувати створення резервної копії
     * або іншу сервісну операцію. У цій реалізації
     * лише виводить повідомлення в консоль.
     */
    public void backup() {
        System.out.println("Backup method called for server '" + name + "'");
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void accept(NetworkVisitor visitor) {
        visitor.visitServer(this);
    }
}