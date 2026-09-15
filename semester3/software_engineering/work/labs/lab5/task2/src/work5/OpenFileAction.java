package work5;

/**
 * Конкретна дія, що моделює відкриття файлу.
 */
public class OpenFileAction implements Action {

    /**
     * Створює дію відкриття файлу.
     */
    public OpenFileAction() {
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void execute() {
        System.out.println("Executing OpenFileAction: opening file...");
    }
}