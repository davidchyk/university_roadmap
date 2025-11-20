package work5;

/**
 * Демонстраційний клас для показу роботи шаблону Command.
 * Створює кілька конкретних дій, макро-дію та ініціатор,
 * демонструє динамічну зміну поведінки без умовних операторів.
 */
public class ActionDemo {

    /**
     * Точка входу в програму.
     * @param args аргументи командного рядка (не використовуються)
     */
    public static void main(String[] args) {
        // Створюємо окремі дії
        Action save = new SaveFileAction();
        Action open = new OpenFileAction();
        Action copy = new CopyAction();
        Action paste = new PasteAction();

        // Створюємо макро-дію (наприклад, "Save All and Backup")
        MacroAction saveAndBackup = new MacroAction();
        saveAndBackup.addAction(save);
        saveAndBackup.addAction(copy);
        saveAndBackup.addAction(paste);

        // Створюємо Invoker
        Invoker invoker = new Invoker();

        // Демонстрація: окремі дії
        invoker.setAction(open);
        invoker.click(); // Open

        invoker.setAction(copy);
        invoker.click(); // Copy

        invoker.setAction(paste);
        invoker.click(); // Paste

        invoker.setAction(save);
        invoker.click(); // Save

        // Демонстрація макро-дії
        invoker.setAction(saveAndBackup);
        invoker.click();
    }
}