package work5;

/**
 * Конкретна дія, що моделює операцію вставки.
 */
public class PasteAction implements Action {

    /**
     * Створює дію вставки.
     */
    public PasteAction() {
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void execute() {
        System.out.println("Executing PasteAction: pasting from clipboard...");
    }
}