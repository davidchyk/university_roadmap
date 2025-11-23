package work5;

/**
 * Демонстрацiйний клас для перевiрки роботи шаблону Singleton
 * та взаємодiї всiх елементiв гри через GameManager
 */
public class GameManagerDemo {

    /**
     * Точка входу в програму
     * @param args параметри командного рядка (не використовуються)
     */
    public static void main(String[] args) {
        // Отримуємо два «екземпляри» розпорядника гри
        GameManager manager1 = GameManager.getInstance();
        GameManager manager2 = GameManager.getInstance();

        System.out.println("Checking Singleton:");
        System.out.println("manager1 == manager2 -> " + (manager1 == manager2));
        System.out.println();

        // Налаштовуємо iгровий простiр через перший посил
        GameSpace space = new GameSpace("Dungeon level", 20, 15);
        manager1.setGameSpace(space);

        // Додаємо кiлька фiшок через другий посил (для демонстрацiї єдиного екземпляра)
        manager2.restartGame(); // починаємо нову гру
        GamePiece hero = new GamePiece(1, "Hero", 5, 5);
        GamePiece monster = new GamePiece(2, "Monster", 10, 7);
        GamePiece chest = new GamePiece(3, "Chest", 3, 2);

        manager2.addPiece(hero);
        manager2.addPiece(monster);
        manager2.addPiece(chest);

        System.out.println("Initial game state (via manager1):");
        manager1.printState();
        System.out.println();

        // Перемiщення фiшки
        System.out.println("Moving piece with id = 2 (Monster) to (12, 8)...");
        manager1.movePiece(2, 12, 8);
        System.out.println("Game state after movement (via manager2):");
        manager2.printState();
        System.out.println();

        // Видалення фiшки
        System.out.println("Removing piece with id = 3 (Chest)...");
        GamePiece toRemove = manager1.findPieceById(3);
        if (toRemove != null) {
            manager1.removePiece(toRemove);
        }
        System.out.println("Game state after removing chest (via manager1):");
        manager1.printState();
        System.out.println();

        // Перезапуск гри
        System.out.println("Restarting game...");
        manager2.restartGame();
        System.out.println("Game state after restart (via manager2):");
        manager2.printState();
    }
}