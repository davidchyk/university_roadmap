package work5;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Singleton-клас розпорядника гри
 * Мiстить iнформацiю про iгровий простiр та всi iгровi фiшки й є
 * єдиною точкою керування грою
 */
public class GameManager {

    /** Єдиний примiрник GameManager */
    private static GameManager instance;

    /** Поточний iгровий простiр */
    private GameSpace gameSpace;

    /** Список усiх фiшок у грi */
    private final List<GamePiece> pieces = new ArrayList<>();

    /** Номер поточної гри (для демонстрацiї перезапуску) */
    private int gameNumber = 0;

    /**
     * Приватний конструктор забороняє створення об’єкта ззовнi
     */
    private GameManager() {
        // початковий порожнiй простiр
        this.gameSpace = new GameSpace("Default space", 10, 10);
    }

    /**
     * Повертає єдиний примiрник розпорядника гри
     * @return єдиний примiрник GameManager
     */
    public static GameManager getInstance() {
        if (instance == null) {
            instance = new GameManager();
        }
        return instance;
    }

    /**
     * Встановлює новий iгровий простiр
     * @param space новий простiр гри
     */
    public void setGameSpace(GameSpace space) {
        if (space == null) {
            throw new IllegalArgumentException("GameSpace cannot be null");
        }
        this.gameSpace = space;
    }

    /**
     * Повертає поточний iгровий простiр
     * @return iгровий простiр
     */
    public GameSpace getGameSpace() {
        return gameSpace;
    }

    /**
     * Додає нову фiшку до гри
     * @param piece фiшка для додавання
     */
    public void addPiece(GamePiece piece) {
        if (piece == null) {
            throw new IllegalArgumentException("GamePiece cannot be null");
        }
        pieces.add(piece);
    }

    /**
     * Видаляє фiшку з гри
     * @param piece фiшка для видалення
     * @return true, якщо фiшку знайдено i видалено
     */
    public boolean removePiece(GamePiece piece) {
        return pieces.remove(piece);
    }

    /**
     * Пошук фiшки за iдентифiкатором
     * @param id iдентифiкатор фiшки
     * @return знайдена фiшка або null, якщо її немає
     */
    public GamePiece findPieceById(int id) {
        for (GamePiece piece : pieces) {
            if (piece.getId() == id) {
                return piece;
            }
        }
        return null;
    }

    /**
     * Перемiщує фiшку з вказаним iдентифiкатором у нову позицiю
     * @param id   iдентифiкатор фiшки
     * @param xNew нова координата X
     * @param yNew нова координата Y
     */
    public void movePiece(int id, int xNew, int yNew) {
        GamePiece piece = findPieceById(id);
        if (piece != null) {
            piece.setX(xNew);
            piece.setY(yNew);
        }
    }

    /**
     * Повертає незмiнний список усiх фiшок
     * @return список фiшок
     */
    public List<GamePiece> getPieces() {
        return Collections.unmodifiableList(pieces);
    }

    /**
     * Запускає або перезапускає гру
     * Для простоти: очищає список фiшок та збiльшує номер гри
     */
    public void restartGame() {
        pieces.clear();
        gameNumber++;
    }

    /**
     * Повертає номер поточної гри
     * @return номер гри
     */
    public int getGameNumber() {
        return gameNumber;
    }

    /**
     * Друкує поточний стан гри в консоль
     * Вивiд виконується англiйською мовою вiдповiдно до вимог
     */
    public void printState() {
        System.out.println("=== Game state ===");
        System.out.println("Game number: " + gameNumber);
        System.out.println("Game space: " + gameSpace);
        System.out.println("Pieces:");
        if (pieces.isEmpty()) {
            System.out.println("  (no pieces)");
        } else {
            for (GamePiece piece : pieces) {
                System.out.println("  " + piece);
            }
        }
        System.out.println("==================");
    }
}