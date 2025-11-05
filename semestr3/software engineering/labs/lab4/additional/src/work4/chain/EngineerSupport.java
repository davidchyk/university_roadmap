package work4.chain;

/**
 * Інженер підтримки — обробляє запити 2-го рівня (середній).
 */
public final class EngineerSupport extends AbstractSupportHandler {
    @Override
    protected boolean canHandle(int level) { return level == 2; }

    @Override
    protected void doHandle(SupportRequest request) {
        System.out.println("EngineerSupport: handled (L2) -> " + request);
    }
}
