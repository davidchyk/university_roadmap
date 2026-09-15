package work5;

/**
 * Конкретна фабрика iнструментiв середовища розробки для мови C++
 */
public class CppIDEToolsFactory implements IDEToolsFactory {

    @Override
    public Validator createValidator() {
        return new CppValidator();
    }

    @Override
    public Compiler createCompiler() {
        return new CppCompiler();
    }

    @Override
    public Debugger createDebugger() {
        return new CppDebugger();
    }
}
