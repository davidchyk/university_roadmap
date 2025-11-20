package work5;

/**
 * Конкретний відвідувач, який обчислює загальну вартість усієї мережі.
 * Реалізує шаблон {@code Visitor}: проходить по всіх елементах мережі
 * та накопичує сумарну вартість.
 */
public class CostCalculatorVisitor implements NetworkVisitor {

    /**
     * Поточне накопичене значення загальної вартості.
     */
    private double totalCost = 0.0;

    /**
     * Повертає обчислену загальну вартість мережі.
     * @return загальна вартість
     */
    public double getTotalCost() {
        return totalCost;
    }

    /**
     * Додає вартість кабелю до загальної суми.
     * @param cable кабель, що відвідується
     */
    @Override
    public void visitCable(Cable cable) {
        totalCost += cable.getCost();
    }

    /**
     * Додає вартість сервера до загальної суми.
     * @param server сервер, що відвідується
     */
    @Override
    public void visitServer(Server server) {
        totalCost += server.getBaseCost();
    }

    /**
     * Додає вартість робочої станції до загальної суми.
     * @param workstation робоча станція, що відвідується
     */
    @Override
    public void visitWorkstation(Workstation workstation) {
        totalCost += workstation.getBaseCost();
    }

    /**
     * Обробляє мережу: обходить усі вкладені елементи.
     * Власна вартість мережі може не враховуватися, якщо
     * не задано додаткових параметрів. У цій реалізації
     * вартість складається лише з дочірніх елементів.
     * @param network мережа, що відвідується
     */
    @Override
    public void visitNetwork(Network network) {
        for (NetworkElement element : network.getElements()) {
            element.accept(this);
        }
    }
}