package lab2;

/**
 * Клас Cl3 успадковує Cl2 та реалізує інтерфейс If3.
 * Реалізує всі методи з виведенням у консоль.
 * @author Artem Davydchuk
 * @version 1.0
 */

public class Cl3 extends Cl2 implements If3 {
    /**
     * Джерело опису: {@link Cl2#meth1()} (транзитивно з {@link If1#meth1()}).
     * {@inheritDoc}
     */
    @Override
    public void meth1() { System.out.println("Cl3: meth1"); }

    /**
     * Джерело опису: {@link Cl2#meth2()} (транзитивно з {@link If1#meth2()}).
     * {@inheritDoc}
     */
    @Override
    public void meth2() { System.out.println("Cl3: meth2"); }

    /**
     * Джерело опису: {@link Cl2#meth3()} (транзитивно з {@link If1#meth3()}).
     * {@inheritDoc}
     */
    @Override
    public void meth3() { System.out.println("Cl3: meth3"); }
}
