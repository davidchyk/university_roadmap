package work4.chain;

/**
 * Старший інженер підтримки — обробляє запити 3-го рівня (складний).
 */
public final class SeniorEngineerSupport extends AbstractSupportHandler {
    @Override
    protected boolean canHandle(int level) { return level == 3; }

    @Override
    protected void doHandle(SupportRequest request) {
        System.out.println("SeniorEngineerSupport: handled (L3) -> " + request);
    }
}
