package work5;

/**
 * Iнтерфейс перевiрки вихiдного коду
 */
public interface Validator {

    /**
     * Виконує перевiрку заданого тексту програми
     * @param code вихiдний код для перевiрки
     */
    void validateCode(String code);
}