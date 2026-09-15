package lab2;

/**
 * Клас Cl2 реалізує інтерфейс If2.
 * Реалізує всі методи базового інтерфейсу If1.
 * @author Artem Davydchuk
 * @version 1.0
 */

public class Cl2 implements If2 {
    /**
     * Джерело опису: {@link If1#meth1()}
     * (через {@link If2}).
     * {@inheritDoc}
     */
    @Override
    public void meth1() { System.out.println("Cl2: meth1"); }

    /**
     * Джерело опису: {@link If1#meth2()} (через {@link If2}).
     * {@inheritDoc}
     */
    @Override
    public void meth2() { System.out.println("Cl2: meth2"); }

    /**
     * Джерело опису: {@link If1#meth3()} (через {@link If2}).
     * {@inheritDoc}
     */
    @Override
    public void meth3() { System.out.println("Cl2: meth3"); }
}
