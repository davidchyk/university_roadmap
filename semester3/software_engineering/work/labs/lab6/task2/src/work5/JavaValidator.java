package work5;

/**
 * Реалiзацiя валiдатора для мови Java
 */
public class JavaValidator implements Validator {

    @Override
    public void validateCode(String code) {
        System.out.println("JavaValidator: validating Java code...");
        System.out.println("  Code: " + code);
        System.out.println("  Result: no syntax errors found.");
    }
}