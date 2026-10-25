public final class T2 extends Worker {
    public T2(Data data, Monitor monitor) {
        super("T2", 1, data, monitor);
    }

    @Override
    public void run() {
        try {
            long b = calculateIntermediate();
            monitor.waitSortFinished();
            calculateResult(b);

            monitor.signalCalculationFinished();
        } catch (InterruptedException e) {
            reportInterruption();
        }
    }
}
