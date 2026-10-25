public abstract class Worker extends Thread {
    protected final Data data;
    protected final Monitor monitor;
    private final int threadIndex;

    protected Worker(String name, int threadIndex, Data data, Monitor monitor) {
        super(name);
        this.threadIndex = threadIndex;
        this.data = data;
        this.monitor = monitor;
    }

    protected final long calculateIntermediate() throws InterruptedException {
        monitor.waitInput();

        int start = data.start(threadIndex);
        int end = data.end(threadIndex);
        data.calculateIntermediatePart(start, end);
        long localB = data.calculateLocalDotProduct(start, end);

        monitor.addPartialBAndSignal(localB);
        return monitor.waitIntermediateAndCopyB();
    }

    protected final void calculateResult(long b) {
        int start = data.start(threadIndex);
        int end = data.end(threadIndex);
        data.calculateResultPart(start, end, b);
    }

    protected final void reportInterruption() {
        Thread.currentThread().interrupt();
        System.err.println(getName() + " was interrupted");
    }
}
