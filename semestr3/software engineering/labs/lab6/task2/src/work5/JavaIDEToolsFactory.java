package work5;

/**
 * Конкретна фабрика iнструментiв середовища розробки для мови Java
 */
public class JavaIDEToolsFactory implements IDEToolsFactory {

    @Override
    public Validator createValidator() {
        return new JavaValidator();
    }

    @Override
    public Compiler createCompiler() {
        return new JavaCompiler();
    }

    @Override
    public Debugger createDebugger() {
        return new JavaDebugger();
    }
}