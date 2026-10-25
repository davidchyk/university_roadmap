import java.util.Scanner;

public final class Monitor {
    private final int threadCount;
    private int inputCount;
    private int intermediateCount;
    private int calculationCount;
    private boolean sortFinished;
    private long b;
    private long startTimeNanos;

    public Monitor(int threadCount) {
        this.threadCount = threadCount;
    }

    // Input methods also protect the shared Scanner and console.
    public synchronized void inputT1(Scanner scanner, Data data) {
        System.out.print("T1: fill value for MM: ");
        Data.fillMatrix(data.MM, scanner.nextLong());
        System.out.print("T1: fill value for B: ");
        Data.fillVector(data.B, scanner.nextLong());
        System.out.print("T1: fill value for MX: ");
        Data.fillMatrix(data.MX, scanner.nextLong());
    }

    public synchronized void inputT3(Scanner scanner, Data data) {
        System.out.print("T3: value for p: ");
        data.p = scanner.nextLong();
    }

    public synchronized void inputT4(Scanner scanner, Data data) {
        System.out.print("T4: fill value for Z: ");
        Data.fillVector(data.Z, scanner.nextLong());
        System.out.print("T4: fill value for MT: ");
        Data.fillMatrix(data.MT, scanner.nextLong());
        System.out.print("T4: value for d: ");
        data.d = scanner.nextLong();
    }

    public synchronized void signalInput() {
        inputCount++;
        if (inputCount == 3) {
            startTimeNanos = System.nanoTime();
        }
        notifyAll();
    }

    public synchronized void waitInput() throws InterruptedException {
        while (inputCount < 3) {
            wait();
        }
    }

    // Atomic reduction b = b + bi and synchronization of intermediate results.
    public synchronized void addPartialBAndSignal(long localB) {
        b += localB;
        intermediateCount++;
        notifyAll();
    }

    public synchronized long waitIntermediateAndCopyB()
            throws InterruptedException {
        while (intermediateCount < threadCount) {
            wait();
        }
        return b;
    }

    public synchronized void signalSortFinished() {
        sortFinished = true;
        notifyAll();
    }

    public synchronized void waitSortFinished() throws InterruptedException {
        while (!sortFinished) {
            wait();
        }
    }

    // T1-T3 notify T4 that their parts of A are ready.
    public synchronized void signalCalculationFinished() {
        calculationCount++;
        notifyAll();
    }

    public synchronized void waitOtherCalculations()
            throws InterruptedException {
        while (calculationCount < threadCount - 1) {
            wait();
        }
    }

    public synchronized double elapsedSeconds() {
        return (System.nanoTime() - startTimeNanos) / 1_000_000_000.0;
    }

    public synchronized void printResult(long[] result) {
        System.out.print("A = [");
        for (int i = 0; i < result.length; i++) {
            if (i > 0) {
                System.out.print(", ");
            }
            System.out.print(result[i]);
        }
        System.out.println("]");
    }
}
