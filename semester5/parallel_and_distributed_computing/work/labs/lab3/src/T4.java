import java.util.Scanner;

public final class T4 extends Worker {
    private final Scanner scanner;

    public T4(Data data, Monitor monitor, Scanner scanner) {
        super("T4", 3, data, monitor);
        this.scanner = scanner;
    }

    @Override
    public void run() {
        try {
            monitor.inputT4(scanner, data);
            monitor.signalInput();

            long b = calculateIntermediate();

            // U is complete after the intermediate synchronization point.
            data.sortU();
            monitor.signalSortFinished();

            calculateResult(b);
            monitor.waitOtherCalculations();
            double elapsed = monitor.elapsedSeconds();
            monitor.printResult(data.A);
            System.out.printf("Computation time: %.6f seconds%n", elapsed);
        } catch (InterruptedException e) {
            reportInterruption();
        }
    }
}
