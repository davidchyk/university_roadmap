package work4.chain;

/**
 * Базовий клас для обробників підтримки.
 * Інкапсулює зберігання посилання на «наступного» та делегування.
 * @pattern Chain of Responsibility: Concrete Handler (base)
 */
public abstract class AbstractSupportHandler implements Handler {
    private Handler next;

    @Override
    public void setNextHandler(Handler nextHandler) {
        this.next = nextHandler;
    }

    /**
     * Перевіряє, чи вміє поточний обробник обслуговувати даний рівень.
     * @param level рівень складності запиту
     * @return true, якщо цей хендлер обробляє такий рівень
     */
    protected abstract boolean canHandle(int level);

    /**
     * Власне обробка (бізнес-заглушка з виводом у консоль).
     * @param request запит
     */
    protected abstract void doHandle(SupportRequest request);

    @Override
    public final void handleRequest(SupportRequest request) {
        if (request == null) return;
        if (canHandle(request.getLevel())) {
            doHandle(request); // обробляємо тут
        } else if (next != null) {
            System.out.println(getClass().getSimpleName()
                    + " -> passing to " + next.getClass().getSimpleName()
                    + " for " + request);
            next.handleRequest(request); // передаємо далі
        } else {
            System.out.println(getClass().getSimpleName()
                    + " -> no next handler, request dropped: " + request);
        }
    }
}
