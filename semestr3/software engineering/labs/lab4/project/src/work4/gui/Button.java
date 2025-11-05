package work4.gui;

/**
 * Конкретний GUI-елемент: кнопка.
 * Генерує подію {@code "click"} методом {@link #click()}.
 */
public final class Button extends GuiElement {
    /**
     * Створює кнопку.
     * @param id   унікальний id
     * @param name назва
     */
    public Button(String id, String name) {
        super(id, name);
    }

    /**
     * Імітує натискання користувачем та підіймає подію {@code "click"}.
     * <p><b>Бізнес-заглушка:</b> друк у консоль.</p>
     */
    public void click() {
        System.out.println("Method click called for " + this);
        fireEvent("click");
    }
}
