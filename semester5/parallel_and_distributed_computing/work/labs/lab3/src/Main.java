/*
 * Дисципліна: Паралельні та розподілені обчислення
 * Лабораторна робота №3.2: Монітори в Java
 * Варіант 16
 * A = p * (sort(d * B + Z * MM) * (MX * MT)) + (B * Z) * Z
 * Виконав: студент групи ІО-41 Давидчук Артем Миколайович
 */

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            System.out.print("Enter N: ");
            int n = scanner.nextInt();
            if (n <= 0) {
                throw new IllegalArgumentException("N must be positive");
            }

            Data data = new Data(n);
            Monitor monitor = new Monitor(4);

            Thread t1 = new T1(data, monitor, scanner);
            Thread t2 = new T2(data, monitor);
            Thread t3 = new T3(data, monitor, scanner);
            Thread t4 = new T4(data, monitor, scanner);

            t1.start();
            t2.start();
            t3.start();
            t4.start();

            t1.join();
            t2.join();
            t3.join();
            t4.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Main thread was interrupted");
        }
    }
}
