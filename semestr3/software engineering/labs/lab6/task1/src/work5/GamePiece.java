package work5;

/**
 * Клас, що описує окрему iгрову фiшку
 */
public class GamePiece {

    /** Унiкальний iдентифiкатор фiшки */
    private final int id;

    /** Тип або назва фiшки (Player, Enemy, NPC тощо) */
    private final String type;

    /** Поточна координата X на полi */
    private int x;

    /** Поточна координата Y на полi */
    private int y;

    /**
     * Створює нову фiшку.

     * @param id   iдентифiкатор фiшки
     * @param type тип або назва фiшки
     * @param x    початкова координата X
     * @param y    початкова координата Y
     */
    public GamePiece(int id, String type, int x, int y) {
        this.id = id;
        this.type = type;
        this.x = x;
        this.y = y;
    }

    /**
     * Повертає iдентифiкатор фiшки
     * @return iдентифiкатор
     */
    public int getId() {
        return id;
    }

    /**
     * Повертає тип фiшки
     * @return тип фiшки
     */
    public String getType() {
        return type;
    }

    /**
     * Повертає поточну координату X
     * @return координата X
     */
    public int getX() {
        return x;
    }

    /**
     * Повертає поточну координату Y
     * @return координата Y
     */
    public int getY() {
        return y;
    }

    /**
     * Встановлює нову координату X
     * @param x нове значення X
     */
    public void setX(int x) {
        this.x = x;
    }

    /**
     * Встановлює нову координату Y
     * @param y нове значення Y
     */
    public void setY(int y) {
        this.y = y;
    }

    @Override
    public String toString() {
        return "GamePiece{id=" + id + ", type='" + type + "', x=" + x + ", y=" + y + "}";
    }
}