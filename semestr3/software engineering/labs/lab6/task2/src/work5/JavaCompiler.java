package work5;

/**
 * Реалiзацiя компiлятора для мови Java
 */
public class JavaCompiler implements Compiler {

    @Override
    public void compile(String source) {
        System.out.println("JavaCompiler: compiling Java source...");
        System.out.println("  Source: " + source);
        System.out.println("  Result: compilation successful, .class file generated.");
    }
}