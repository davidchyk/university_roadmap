package work5;

/**
 * Елемент мережі, що представляє робочу станцію користувача.
 * Містить інформацію про базову вартість та власника.
 * Підтримує шаблон {@code Visitor} через інтерфейс
 * {@link NetworkElement}.
 */
public class Workstation implements NetworkElement {

    /**
     * Назва робочої станції.
     */
    private final String name;

    /**
     * Базова вартість робочої станції.
     */
    private final double baseCost;

    /**
     * Ім'я власника робочої станції.
     */
    private final String owner;

    /**
     * Створює нову робочу станцію.
     * @param name     назва робочої станції
     * @param baseCost базова вартість
     * @param owner    власник робочої станції
     */
    public Workstation(String name, double baseCost, String owner) {
        this.name = name;
        this.baseCost = baseCost;
        this.owner = owner;
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public String getName() {
        return name;
    }

    /**
     * Повертає базову вартість робочої станції.
     * @return базова вартість
     */
    public double getBaseCost() {
        return baseCost;
    }

    /**
     * Повертає ім'я власника.
     * @return власник робочої станції
     */
    public String getOwner() {
        return owner;
    }

    /**
     * Бізнес-метод із заглушкою.
     * Може відповідати запуску діагностики системи.
     * Наразі лише виводить повідомлення в консоль.
     */
    public void runDiagnostics() {
        System.out.println("Diagnostics started for workstation '" + name + "'");
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void accept(NetworkVisitor visitor) {
        visitor.visitWorkstation(this);
    }
}