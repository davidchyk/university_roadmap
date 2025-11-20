package work5;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Композитний елемент мережі, що представляє логічну мережу або підмережу.
 * Реалізує шаблон {@code Composite}: мережа може містити окремі елементи
 * ({@link Cable}, {@link Server}, {@link Workstation}) та інші об'єкти {@link Network}.
 * Також підтримує шаблон {@code Visitor} через інтерфейс {@link NetworkElement}.
 */
public class Network implements NetworkElement {

    /**
     * Назва мережі.
     */
    private final String name;

    /**
     * Список вкладених елементів мережі.
     */
    private final List<NetworkElement> elements = new ArrayList<>();

    /**
     * Створює мережу з указаною назвою.
     * @param name назва мережі
     */
    public Network(String name) {
        this.name = name;
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public String getName() {
        return name;
    }

    /**
     * Додає елемент до мережі.
     * @param element елемент мережі для додавання
     */
    public void addElement(NetworkElement element) {
        elements.add(element);
    }

    /**
     * Видаляє елемент з мережі.
     * @param element елемент мережі для видалення
     */
    public void removeElement(NetworkElement element) {
        elements.remove(element);
    }

    /**
     * Повертає немодифікований список вкладених елементів.
     * @return список елементів мережі
     */
    public List<NetworkElement> getElements() {
        return Collections.unmodifiableList(elements);
    }

    /**
     * Бізнес-метод із заглушкою.
     * Може моделювати перевірку стану мережі. Тут обмежується
     * лише виведенням текстового повідомлення.
     */
    public void checkStatus() {
        System.out.println("Checking status for network '" + name + "'");
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void accept(NetworkVisitor visitor) {
        visitor.visitNetwork(this);
    }
}