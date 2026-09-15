package work5;

/**
 * Абстрактна фабрика iнструментiв iнтегрованого середовища розробки
 * Визначає фабричнi методи для створення об'єктiв типiв
 * {@link Validator}, {@link Compiler} та {@link Debugger}
 */
public interface IDEToolsFactory {

    /**
     * Створює об'єкт перевiрки коду
     * @return екземпляр валiдатора
     */
    Validator createValidator();

    /**
     * Створює об'єкт компiлятора
     * @return екземпляр компiлятора
     */
    Compiler createCompiler();

    /**
     * Створює об'єкт налагоджувача
     * @return екземпляр дебагера
     */
    Debugger createDebugger();
}