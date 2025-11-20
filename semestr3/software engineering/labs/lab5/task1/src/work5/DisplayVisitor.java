package work5;

/**
 * Конкретний відвідувач, який виводить структуру мережі у вигляді дерева.
 * Для кожного рівня вкладеності додає відступи, щоб
 * продемонструвати ієрархію елементів.
 */
public class DisplayVisitor implements NetworkVisitor {

    /**
     * Поточний рівень відступу (глибина вкладеності).
     */
    private int indentLevel = 0;

    /**
     * Друкує відступи відповідно до поточного рівня.
     */
    private void printIndent() {
        for (int i = 0; i < indentLevel; i++) {
            System.out.print("  ");
        }
    }

    /**
     * Виводить інформацію про кабель.
     * @param cable кабель, що відвідується
     */
    @Override
    public void visitCable(Cable cable) {
        printIndent();
        System.out.println("Cable: " + cable.getName()
                + " (length=" + cable.getLengthMeters() + "m)");
    }

    /**
     * Виводить інформацію про сервер.
     * @param server сервер, що відвідується
     */
    @Override
    public void visitServer(Server server) {
        printIndent();
        System.out.println("Server: " + server.getName()
                + " (cost=" + server.getBaseCost()
                + ", cores=" + server.getCpuCores() + ")");
    }

    /**
     * Виводить інформацію про робочу станцію.
     * @param workstation робоча станція, що відвідується
     */
    @Override
    public void visitWorkstation(Workstation workstation) {
        printIndent();
        System.out.println("Workstation: " + workstation.getName()
                + " (cost=" + workstation.getBaseCost()
                + ", owner=" + workstation.getOwner() + ")");
    }

    /**
     * Виводить інформацію про мережу та рекурсивно
     * обходить усі її дочірні елементи.
     * @param network мережа, що відвідується
     */
    @Override
    public void visitNetwork(Network network) {
        printIndent();
        System.out.println("Network: " + network.getName());
        indentLevel++;
        for (NetworkElement element : network.getElements()) {
            element.accept(this);
        }
        indentLevel--;
    }
}