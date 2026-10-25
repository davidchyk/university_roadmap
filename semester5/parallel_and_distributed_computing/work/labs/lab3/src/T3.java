import java.util.Scanner;

public final class T3 extends Worker {
    private final Scanner scanner;

    public T3(Data data, Monitor monitor, Scanner scanner) {
        super("T3", 2, data, monitor);
        this.scanner = scanner;
    }

    @Override
    public void run() {
        try {
            monitor.inputT3(scanner, data);
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
