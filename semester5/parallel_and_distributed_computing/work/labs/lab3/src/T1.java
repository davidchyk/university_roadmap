import java.util.Scanner;

public final class T1 extends Worker {
    private final Scanner scanner;

    public T1(Data data, Monitor monitor, Scanner scanner) {
        super("T1", 0, data, monitor);
        this.scanner = scanner;
    }

    @Override
    public void run() {
        try {
            monitor.inputT1(scanner, data);
            monitor.signalInput();

            long b = calculateIntermediate();
            monitor.waitSortFinished();
            calculateResult(b);

            monitor.signalCalculationFinished();
        } catch (InterruptedException e) {
            reportInterruption();
        }
    }
}
