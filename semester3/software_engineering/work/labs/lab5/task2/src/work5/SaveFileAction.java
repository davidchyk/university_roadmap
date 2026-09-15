package work5;

/**
 * Конкретна дія, що моделює збереження файлу.
 */
public class SaveFileAction implements Action {

    /**
     * Створює дію збереження файлу.
     */
    public SaveFileAction() {
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void execute() {
        System.out.println("Executing SaveFileAction: saving file...");
    }
}