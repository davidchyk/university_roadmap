package work4.gui;

/**
 * Конкретний GUI-елемент: однорядкове текстове поле.
 * Підіймає подію {@code "textChanged"} при оновленні тексту.
 */
public final class TextField extends GuiElement {
    /** Поточний текст. */
    private String text = "";

    /**
     * Створює текстове поле.
     * @param id   унікальний id
     * @param name назва
     */
    public TextField(String id, String name) {
        super(id, name);
    }

    /** @return поточне значення тексту */
    public String getText() { return text; }

    /**
     * Встановлює текст і публікує подію {@code "textChanged"}.
     * <p><b>Бізнес-заглушка:</b> друк параметрів у консоль.</p>
     * @param text нове значення тексту
     */
    public void setText(String text) {
        System.out.println("Method setText called with text=" + text);
        this.text = text;
        fireEvent("textChanged");
    }
}
