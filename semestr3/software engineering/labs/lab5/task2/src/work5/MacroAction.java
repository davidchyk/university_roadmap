package work5;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Макро-дія, що представляє собою послідовність інших дій.
 * Реалізує інтерфейс {@link Action} та при виклику {@link #execute()}
 * послідовно виконує всі вкладені команди.
 */
public class MacroAction implements Action {

    /**
     * Список дій, що входять до макро-команди.
     */
    private final List<Action> actions = new ArrayList<>();

    /**
     * Створює порожню макро-дію.
     */
    public MacroAction() {
    }

    /**
     * Додає нову дію до макро-команди.
     * @param action дія для додавання
     */
    public void addAction(Action action) {
        if (action != null) {
            actions.add(action);
        }
    }

    /**
     * Повертає немодифікований список вкладених дій.
     * @return список дій
     */
    public List<Action> getActions() {
        return Collections.unmodifiableList(actions);
    }

    /**
     * {@inheritDoc}
     * Послідовно викликає {@code execute()} для кожної вкладеної дії.
     */
    @Override
    public void execute() {
        System.out.println("Executing MacroAction: starting sequence...");
        for (Action action : actions) {
            action.execute();
        }
        System.out.println("Executing MacroAction: sequence finished.");
    }
}