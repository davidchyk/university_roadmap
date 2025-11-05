package work4.gui;

import java.util.*;

/**
 * Конкретний GUI-елемент: вікно з заголовком і дочірніми елементами.
 * Підіймає подію {@code "close"} при виклику {@link #close()}.
 */
public final class Window extends GuiElement {
    /** Заголовок вікна. */
    private String title;
    /** Дочірні елементи вікна. */
    private final List<GuiElement> children = new ArrayList<>();

    /**
     * Створює вікно.
     * @param id    унікальний id
     * @param name  назва
     * @param title початковий заголовок
     */
    public Window(String id, String name, String title) {
        super(id, name);
        this.title = Objects.requireNonNull(title, "title");
    }

    /** @return поточний заголовок вікна */
    public String getTitle() { return title; }

    /**
     * Встановлює заголовок вікна.
     * <p><b>Бізнес-заглушка:</b> друк параметрів у консоль.</p>
     * @param title новий заголовок
     */
    public void setTitle(String title) {
        System.out.println("Method setTitle called with title=" + title);
        this.title = title;
    }

    /**
     * Додає дочірній елемент.
     * <p><b>Бізнес-заглушка:</b> друк параметрів у консоль.</p>
     * @param child елемент, який додається
     */
    public void addChild(GuiElement child) {
        System.out.println("Method addChild called with child=" + child);
        children.add(child);
    }

    /**
     * Видаляє дочірній елемент.
     * <p><b>Бізнес-заглушка:</b> друк параметрів у консоль.</p>
     * @param child елемент, який видаляється
     */
    public void removeChild(GuiElement child) {
        System.out.println("Method removeChild called with child=" + child);
        children.remove(child);
    }

    /**
     * Закриває вікно та публікує подію {@code "close"}.
     * <p><b>Бізнес-заглушка:</b> друк у консоль.</p>
     */
    public void close() {
        System.out.println("Method close called for " + this + " (title=\"" + title + "\")");
        fireEvent("close");
    }

    /**
     * Повертає немодифікований знімок списку дочірніх елементів.
     * @return лише для читання список дочірніх елементів
     */
    public List<GuiElement> getChildren() {
        return Collections.unmodifiableList(children);
    }
}
