package work5;

/**
 * Iнтерфейс компiлятора вихiдного коду
 */
public interface Compiler {

    /**
     * Компiлює заданий текст програми
     * @param source вихiдний код для компiляцiї
     */
    void compile(String source);
}