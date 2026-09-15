package work4.gui;

/**
 * Слухач дій, який виконує побічні ефекти у відповідь на події.
 * Для демонстрації: при {@code "click"} на кнопці — записує повідомлення у цільове TextField.
 */
public final class ActionHandler implements EventListener {
    /** Текстове поле, що оновлюється при певних подіях. */
    private final TextField target;

    /**
     * Створює обробник дій.
     * @param target текстове поле, яке оновлюватиметься
     */
    public ActionHandler(TextField target) {
        this.target = target;
    }

    /**
     * Реагує на події {@code "click"}, {@code "textChanged"} та {@code "close"}.
     * <p><b>Бізнес-заглушка:</b> друкує дії у консоль.</p>
     *
     * @param eventType тип події
     * @param source    джерело події
     */
    @Override
    public void handleEvent(String eventType, GuiElement source) {
        if ("click".equals(eventType) && source instanceof Button) {
            System.out.println("ActionHandler: button clicked " + source + " -> updating TextField");
            target.setText("Button was clicked!");
        } else if ("textChanged".equals(eventType) && source instanceof TextField) {
            System.out.println("ActionHandler: text changed in " + source);
        } else if ("close".equals(eventType) && source instanceof Window) {
            System.out.println("ActionHandler: window closed -> performing cleanup");
        }
    }
}
