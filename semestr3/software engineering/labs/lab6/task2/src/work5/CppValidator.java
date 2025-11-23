package work5;

/**
 * Реалiзацiя валiдатора для мови C++
 */
public class CppValidator implements Validator {

    @Override
    public void validateCode(String code) {
        System.out.println("CppValidator: validating C++ code...");
        System.out.println("  Code: " + code);
        System.out.println("  Result: no syntax errors found.");
    }
}