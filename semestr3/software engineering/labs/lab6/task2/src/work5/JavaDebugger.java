package work5;

/**
 * Реалiзацiя налагоджувача для мови Java
 */
public class JavaDebugger implements Debugger {

    @Override
    public void debug(String program) {
        System.out.println("JavaDebugger: starting Java debug session...");
        System.out.println("  Program: " + program);
        System.out.println("  Result: breakpoint hit at line 42.");
    }
}