package lab2;

import java.util.ArrayList;
import java.util.List;

/**
 * Клас Cl1 реалізує інтерфейс If1.
 * Містить поля-агрегації: об'єкти Cl2, Cl3 і список власних екземплярів (self-aggregation).
 * Кожен метод виводить у консоль своє ім’я для демонстрації викликів.
 * @author Artem Davydchuk
 * @version 1.0
 */
public class Cl1 implements If1 {
    /** Агрегований об'єкт типу Cl2.
    * @uml.aggregation */
    private Cl2 part2;

    /** Агрегований об'єкт типу Cl3.
     * @uml.aggregation */
    private Cl3 part3;

    /** Список підлеглих екземплярів Cl1 (самоагрегація). */

    private List<Cl1> children = new ArrayList<>();

    /**
     * Джерело опису: {@link If1#meth1()}.
     * {@inheritDoc}
     */
    @Override
    public void meth1() { System.out.println("Cl1: meth1"); }

    /**
     * Джерело опису: {@link If1#meth2()}.
     * {@inheritDoc}
     */
    @Override
    public void meth2() { System.out.println("Cl1: meth2"); }

    /**
     * Джерело опису: {@link If1#meth3()}.
     * {@inheritDoc}
     */
    @Override
    public void meth3() { System.out.println("Cl1: meth3"); }

    /**
     * Задає агрегований об'єкт типу Cl2.
     * @param p екземпляр Cl2
     */
    public void setPart2(Cl2 p) { this.part2 = p; }

    /**
     * Задає агрегований об'єкт типу Cl3.
     * @param p екземпляр Cl3
     */
    public void setPart3(Cl3 p) { this.part3 = p; }

    /**
     * Додає дочірній екземпляр Cl1 до списку.
     * @param child підлеглий об'єкт Cl1
     */
    public void addChild(Cl1 child) { this.children.add(child); }
}
