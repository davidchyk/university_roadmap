package work4.chain;

/**
 * Запит на підтримку.
 */
public final class SupportRequest {
    /** Опис запиту. */
    private final String description;
    /**
     * Рівень складності: 1 — простий, 2 — середній, 3 — складний.
     */
    private final int level;

    /**
     * @param description опис запиту
     * @param level рівень складності (1, 2 або 3)
     */
    public SupportRequest(String description, int level) {
        this.description = description;
        this.level = level;
    }

    /** @return опис запиту */
    public String getDescription() { return description; }

    /** @return рівень складності (1..3) */
    public int getLevel() { return level; }

    @Override
    public String toString() {
        return "SupportRequest{level=" + level + ", desc=\"" + description + "\"}";
    }
}
