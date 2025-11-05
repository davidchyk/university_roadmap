package work4.gui;

/**
 * Інтерфейс спостерігача (слухача) подій GUI.
 * @pattern Observer: Observer (Subscriber)
 */
public interface EventListener {
    /**
     * Обробляє подію, яку згенерував GUI-елемент.
     *
     * @param eventType тип події (напр., {@code "click"}, {@code "textChanged"}, {@code "close"})
     * @param source    джерело події (GUI-елемент)
     */
    void handleEvent(String eventType, GuiElement source);
}
