package lab2;

/**
 * Клас Main призначений для тестування реалізованих класів і інтерфейсів.
 * Демонструє виклики методів і створення агрегованих зв'язків.
 * @author Artem Davydchuk
 * @version 1.0
 */

public class Main {
    /**
     * Точка входу до програми.
     * @param args аргументи командного рядка
     */
    public static void main(String[] args) {
        Cl1 c1 = new Cl1();
        Cl2 c2 = new Cl2();
        Cl3 c3 = new Cl3();

        // Агрегація
        c1.setPart2(c2);
        c1.setPart3(c3);
        c1.addChild(new Cl1());

        // Виклик методів
        c1.meth1();
        c2.meth2();
        c3.meth3();
    }
}
