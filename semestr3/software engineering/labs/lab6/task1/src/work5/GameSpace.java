package work5;

/**
 * Опис iгрового простору (поле, карта, рiвень і ь.д.)
 */
public class GameSpace {

    /** Назва iгрового простору */
    private final String name;

    /** Ширина поля в умовних одиницях */
    private final int width;

    /** Висота поля в умовних одиницях */
    private final int height;

    /**
     * Створює новий iгровий простiр
     * @param name   назва простору
     * @param width  ширина поля
     * @param height висота поля
     */
    public GameSpace(String name, int width, int height) {
        this.name = name;
        this.width = width;
        this.height = height;
    }

    /**
     * Повертає назву простору
     * @return назва iгрового простору
     */
    public String getName() {
        return name;
    }

    /**
     * Повертає ширину поля
     * @return ширина поля
     */
    public int getWidth() {
        return width;
    }

    /**
     * Повертає висоту поля
     * @return висота поля
     */
    public int getHeight() {
        return height;
    }

    @Override
    public String toString() {
        return "GameSpace{name='" + name + "', width=" + width + ", height=" + height + "}";
    }
}