package work4.gui;

import java.util.*;

/**
 * Слухач-логер, що друкує події у консоль.
 * Може мати «білий список» типів подій.
 */
public final class LoggerListener implements EventListener {
    /** Назва логера (напр., "L1"). */
    private final String name;
    /** Фільтр типів подій; порожній означає «логувати все». */
    private final Set<String> filter;

    /**
     * Створює логер.
     * @param name       назва логера
     * @param eventTypes необов’язковий білий список типів подій
     */
    public LoggerListener(String name, String... eventTypes) {
        this.name = Objects.requireNonNull(name, "name");
        this.filter = new HashSet<>(Arrays.asList(eventTypes));
    }

    /**
     * Логує подію, якщо вона проходить фільтр.
     * @param eventType тип події
     * @param source    джерело події
     */
    @Override
    public void handleEvent(String eventType, GuiElement source) {
        if (filter.isEmpty() || filter.contains(eventType)) {
            System.out.println("[" + name + "] event=" + eventType + " source=" + source);
        }
    }
}
