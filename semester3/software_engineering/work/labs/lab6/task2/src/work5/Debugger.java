package work5;

/**
 * Iнтерфейс налагоджувача програми
 */
public interface Debugger {

    /**
     * Запускає процес налагодження заданої програми
     * @param program iдентифiкатор або назва програми для налагодження
     */
    void debug(String program);
}