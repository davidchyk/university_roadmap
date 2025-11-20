package work5;

/**
 * Інтерфейс відвідувача для елементів мережі.
 * Описує набір операцій, які можуть бути виконані над
 * кожним конкретним типом елемента мережі. Додавання
 * нової операції здійснюється шляхом створення нового
 * класу, що реалізує цей інтерфейс.
 */
public interface NetworkVisitor {

    /**
     * Виконує операцію над кабелем.
     * @param cable кабель, який відвідується
     */
    void visitCable(Cable cable);

    /**
     * Виконує операцію над сервером.
     * @param server сервер, який відвідується
     */
    void visitServer(Server server);

    /**
     * Виконує операцію над робочою станцією.
     * @param workstation робоча станція, яка відвідується
     */
    void visitWorkstation(Workstation workstation);

    /**
     * Виконує операцію над мережею (композитним елементом).
     * @param network мережа, яка відвідується
     */
    void visitNetwork(Network network);
}