package work5;

/**
 * Реалiзацiя налагоджувача для мови C++
 */
public class CppDebugger implements Debugger {

    @Override
    public void debug(String program) {
        System.out.println("CppDebugger: starting C++ debug session...");
        System.out.println("  Program: " + program);
        System.out.println("  Result: watchpoint triggered on variable x.");
    }
}