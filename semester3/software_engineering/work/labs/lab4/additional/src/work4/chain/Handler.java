package work4.chain;

/**
 * Інтерфейс співробітника підтримки.
 * @pattern Chain of Responsibility: Handler
 */
public interface Handler {
    /**
     * Обробити запит або передати далі по ланцюжку.
     * @param request запит на підтримку
     */
    void handleRequest(SupportRequest request);

    /**
     * Встановити наступного обробника в ланцюжку.
     * @param nextHandler наступний обробник
     */
    void setNextHandler(Handler nextHandler);
}
