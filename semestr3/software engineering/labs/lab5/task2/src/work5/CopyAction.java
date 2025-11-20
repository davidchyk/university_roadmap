package work5;

/**
 * Конкретна дія, що моделює операцію копіювання.
 */
public class CopyAction implements Action {

    /**
     * Створює дію копіювання.
     */
    public CopyAction() {
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void execute() {
        System.out.println("Executing CopyAction: copying selection...");
    }
}