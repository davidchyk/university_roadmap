package work4.chain;

/**
 * Оператор підтримки — обробляє запити 1-го рівня (простий).
 */
public final class OperatorSupport extends AbstractSupportHandler {
    @Override
    protected boolean canHandle(int level) { return level == 1; }

    @Override
    protected void doHandle(SupportRequest request) {
        System.out.println("OperatorSupport: handled (L1) -> " + request);
    }
}
