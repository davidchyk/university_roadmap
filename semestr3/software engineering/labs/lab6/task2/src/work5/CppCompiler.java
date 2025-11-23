package work5;

/**
 * Реалiзацiя компiлятора для мови C++
 */
public class CppCompiler implements Compiler {

    @Override
    public void compile(String source) {
        System.out.println("CppCompiler: compiling C++ source...");
        System.out.println("  Source: " + source);
        System.out.println("  Result: compilation successful, executable generated.");
    }
}