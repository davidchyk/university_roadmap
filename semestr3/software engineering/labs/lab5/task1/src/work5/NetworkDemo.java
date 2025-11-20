package work5;
    
/**
 * Демонстраційний клас з методом {@code main}, що показує
 * використання шаблонів {@code Composite} та {@code Visitor}
 * для моделювання мережевої структури.
 */
public class NetworkDemo {

    /**
     * Точка входу в програму.
     * Створює приклад структури мережі, демонструє виклик
     * бізнес-методів-заглушок та використання відвідувачів
     * для відображення конфігурації та розрахунку вартості.
     *
     * @param args аргументи командного рядка (не використовуються)
     */
    public static void main(String[] args) {

        // 1. Створення елементів мережі
        Server dbServer = new Server("DB-Server", 5000, 16);
        Workstation ws1 = new Workstation("WS-01", 1200, "Artem");
        Workstation ws2 = new Workstation("WS-02", 1100, "Andrii");

        Cable mainCable = new Cable("Backbone-1", 100, 15);
        Cable ws1Cable = new Cable("Cable-WS1", 20, 10);
        Cable ws2Cable = new Cable("Cable-WS2", 25, 10);

        Network office1 = new Network("Office #1");
        office1.addElement(ws1);
        office1.addElement(ws1Cable);

        Network office2 = new Network("Office #2");
        office2.addElement(ws2);
        office2.addElement(ws2Cable);

        Network rootNetwork = new Network("Head Office LAN");
        rootNetwork.addElement(dbServer);
        rootNetwork.addElement(mainCable);
        rootNetwork.addElement(office1);
        rootNetwork.addElement(office2);

        // 2. Демонстрація бізнес-методів із заглушками
        dbServer.backup();
        ws1.runDiagnostics();
        rootNetwork.checkStatus();

        // 3. Відображення структури мережі
        System.out.println();
        System.out.println("=== Network structure ===");
        DisplayVisitor displayVisitor = new DisplayVisitor();
        rootNetwork.accept(displayVisitor);

        // 4. Розрахунок загальної вартості мережі
        CostCalculatorVisitor costVisitor = new CostCalculatorVisitor();
        rootNetwork.accept(costVisitor);
        System.out.println();
        System.out.println("Total network cost: " + costVisitor.getTotalCost());
    }
}