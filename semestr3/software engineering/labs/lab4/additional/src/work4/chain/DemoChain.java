package work4.chain;

/**
 * Демонстрація ланцюжка: оператор -> інженер -> старший інженер.
 * Показує обробку запитів різної складності та передачу далі.
 */
public class DemoChain {
    public static void main(String[] args) {
        // Побудова ланцюжка
        Handler operator = new OperatorSupport();
        Handler engineer = new EngineerSupport();
        Handler senior   = new SeniorEngineerSupport();

        operator.setNextHandler(engineer);
        engineer.setNextHandler(senior);

        // Кілька прикладів
        SupportRequest r1 = new SupportRequest("Password reset", 1);
        SupportRequest r2 = new SupportRequest("VPN not connecting", 2);
        SupportRequest r3 = new SupportRequest("Production outage", 3);
        SupportRequest rX = new SupportRequest("Exotic issue", 99); // ніхто не візьме

        operator.handleRequest(r1);
        operator.handleRequest(r2);
        operator.handleRequest(r3);
        operator.handleRequest(rX);
    }
}