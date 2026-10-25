import java.util.Arrays;

public final class Data {
    public final int n;

    // Input data
    public final long[] B;
    public final long[] Z;
    public final long[][] MM;
    public final long[][] MX;
    public final long[][] MT;
    public long d;
    public long p;

    // Intermediate and result data
    public final long[] U;
    public final long[][] MC;
    public final long[] A;

    public Data(int n) {
        this.n = n;
        B = new long[n];
        Z = new long[n];
        MM = new long[n][n];
        MX = new long[n][n];
        MT = new long[n][n];
        U = new long[n];
        MC = new long[n][n];
        A = new long[n];
    }

    public static void fillVector(long[] vector, long value) {
        Arrays.fill(vector, value);
    }

    public static void fillMatrix(long[][] matrix, long value) {
        for (long[] row : matrix) {
            Arrays.fill(row, value);
        }
    }

    public int start(int threadIndex) {
        return threadIndex * n / 4;
    }

    public int end(int threadIndex) {
        return (threadIndex + 1) * n / 4;
    }

    public void calculateIntermediatePart(int start, int end) {
        // UH = d * BH + Z * MMH
        for (int j = start; j < end; j++) {
            long sum = 0;
            for (int k = 0; k < n; k++) {
                sum += Z[k] * MM[k][j];
            }
            U[j] = d * B[j] + sum;
        }

        // MCH = MX * MTH
        for (int i = 0; i < n; i++) {
            for (int j = start; j < end; j++) {
                long sum = 0;
                for (int k = 0; k < n; k++) {
                    sum += MX[i][k] * MT[k][j];
                }
                MC[i][j] = sum;
            }
        }
    }

    public long calculateLocalDotProduct(int start, int end) {
        long local = 0;
        for (int i = start; i < end; i++) {
            local += B[i] * Z[i];
        }
        return local;
    }

    public void sortU() {
        Arrays.sort(U);
    }

    public void calculateResultPart(int start, int end, long b) {
        // AH = p * (sort(U) * MCH) + b * ZH
        for (int j = start; j < end; j++) {
            long sum = 0;
            for (int k = 0; k < n; k++) {
                sum += U[k] * MC[k][j];
            }
            A[j] = p * sum + b * Z[j];
        }
    }
}
