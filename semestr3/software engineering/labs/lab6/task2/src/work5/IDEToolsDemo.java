package work5;

/**
 * Демонстрацiйний клас для перевiрки роботи абстрактної фабрики
 * iнструментiв iнтегрованого середовища розробки
 */
public class IDEToolsDemo {

    /**
     * Точка входу в програму
     * @param args параметри командного рядка (не використовуються)
     */
    public static void main(String[] args) {
        System.out.println("Using Java IDE tools factory:");
        IDEToolsFactory javaFactory = new JavaIDEToolsFactory();
        runDemo(javaFactory,
                "System.out.println(\"Hello, Java!\");",
                "JavaSampleProgram");
        System.out.println();

        System.out.println("Using C++ IDE tools factory:");
        IDEToolsFactory cppFactory = new CppIDEToolsFactory();
        runDemo(cppFactory,
                "std::cout << \"Hello, C++!\" << std::endl;",
                "CppSampleProgram");
    }

    /**
     * Допомiжний метод для демонстрацiї роботи фабрики:
     * створює всi iнструменти та послiдовно викликає їх методи
     * @param factory     фабрика iнструментiв
     * @param sampleCode  зразок вихiдного коду
     * @param programName назва програми для налагодження
     */
    private static void runDemo(IDEToolsFactory factory,
                                String sampleCode,
                                String programName) {

        Validator validator = factory.createValidator();
        Compiler compiler = factory.createCompiler();
        Debugger debugger = factory.createDebugger();

        validator.validateCode(sampleCode);
        compiler.compile(sampleCode);
        debugger.debug(programName);
    }
}