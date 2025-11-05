package work4.gui;

import java.util.*;

/**
 * Базовий клас GUI-елемента (Window, Button, TextField).
 * <p>Містить ідентифікатор, назву, стан видимості та набір слухачів подій.
 * Публікує події слухачам через {@link #fireEvent(String)}.</p>
 * @pattern Observer: Subject (Publisher)
 */
public abstract class GuiElement {
    /** Унікальний ідентифікатор елемента. */
    private final String id;
    /** Людинозрозуміла назва елемента. */
    private String name;
    /** Прапорець видимості елемента. */
    private boolean visible = true;
    /** Зареєстровані слухачі подій цього елемента. */
    private final java.util.Set<EventListener> listeners = new java.util.LinkedHashSet<>();

    /**
     * Створює GUI-елемент.
     * @param id   унікальний ідентифікатор (не {@code null})
     * @param name назва для відображення (не {@code null})
     * @throws NullPointerException якщо {@code id} або {@code name} дорівнює {@code null}
     */
    protected GuiElement(String id, String name) {
        this.id = Objects.requireNonNull(id, "id");
        this.name = Objects.requireNonNull(name, "name");
    }

    /** @return незмінний унікальний ідентифікатор елемента */
    public String getId() { return id; }

    /** @return поточна назва елемента */
    public String getName() { return name; }

    /**
     * Встановлює нову назву елемента.
     * <p><b>Бізнес-заглушка:</b> друкує параметри в консоль.</p>
     * @param name нова назва
     */
    public void setName(String name) {
        System.out.println("Method setName called with name=" + name);
        this.name = name;
    }

    /** @return чи є елемент видимим */
    public boolean isVisible() { return visible; }

    /**
     * Показує елемент.
     * <p><b>Бізнес-заглушка:</b> друк у консоль.</p>
     */
    public void show() {
        visible = true;
        System.out.println(getClass().getSimpleName() + "[" + id + "] show()");
    }

    /**
     * Ховає елемент.
     * <p><b>Бізнес-заглушка:</b> друк у консоль.</p>
     */
    public void hide() {
        visible = false;
        System.out.println(getClass().getSimpleName() + "[" + id + "] hide()");
    }

    /**
     * Підписує слухача на події цього елемента.
     * @param l слухач (не {@code null})
     * @throws NullPointerException якщо {@code l} дорівнює {@code null}
    */
    public void addListener(EventListener l) {
        listeners.add(Objects.requireNonNull(l, "listener"));
    }

    /**
     * Відписує слухача від подій цього елемента.
     * @param l слухач для видалення (ігнорується, якщо не підписаний)
     */
    public void removeListener(EventListener l) {
        listeners.remove(l);
    }

    /**
     * Сповіщає всіх зареєстрованих слухачів про подію.
     * <p>Захищений метод: публікувати події має лише сам елемент або нащадки.</p>
     * @param eventType назва типу події
     */
    protected void fireEvent(String eventType) {
        for (EventListener l : listeners) {
            l.handleEvent(eventType, this);
        }
    }

    /** @return коротке відлагоджувальне подання з id та name */
    @Override public String toString() {
        return getClass().getSimpleName() + "{id=" + id + ", name=" + name + "}";
    }
}
