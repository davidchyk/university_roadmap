package work5;

/**
 * Клас-ініціатор, який відповідає за "натискання" кнопок
 * та делегування виконання поточній дії.
 * Містить посилання на об'єкт {@link Action}. Зміна поточної дії
 * дозволяє динамічно змінювати реакцію без використання умовних
 * операторів {@code if}/{@code switch}.
 */
public class Invoker {

    /**
     * Поточна дія, що виконується при натисканні.
     */
    private Action currentAction;

    /**
     * Створює ініціатор без заданої поточної дії.
     */
    public Invoker() {
    }

    /**
     * Встановлює поточну дію.
     * @param action нова дія, яка буде виконуватися
     */
    public void setAction(Action action) {
        this.currentAction = action;
    }

    /**
     * Симулює натискання кнопки або вибір пункту меню.
     * Якщо поточну дію встановлено, викликається її метод {@link Action#execute()}.
     */
    public void click() {
        if (currentAction != null) {
            System.out.println("Invoker: triggering current action...");
            currentAction.execute();
        } else {
            System.out.println("Invoker: no action is set.");
        }
    }
}