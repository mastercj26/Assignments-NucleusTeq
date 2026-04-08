package Chetan_jain_java_training.session1;


import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class FibonacciGenerator {

    private final int FIRST_FIB = 0;
    private final int SECOND_FIB = 1;

    private List<Integer> generateUpTo(int limit) {
        List<Integer> sequence = new ArrayList<>();

        if (limit < FIRST_FIB) {
            return sequence;
        }

        int first = FIRST_FIB;
        int second = SECOND_FIB;

        sequence.add(first);

        if (limit >= SECOND_FIB) {
            sequence.add(second);
        }

        while (true) {
            int next = first + second;
            if (next > limit) {
                break;
            }
            sequence.add(next);
            first = second;
            second = next;
        }

        return sequence;
    }

    private List<Integer> generateFirstN(int count) {
        List<Integer> sequence = new ArrayList<>();

        if (count <= 0) {
            return sequence;
        }

        int first = FIRST_FIB;
        int second = SECOND_FIB;

        sequence.add(first);

        if (count > 1) {
            sequence.add(second);
        }

        for (int i = 2; i < count; i++) {
            int next = first + second;
            sequence.add(next);
            first = second;
            second = next;
        }

        return sequence;
    }

    private void displaySequence(List<Integer> sequence) {
        System.out.println("Fibonacci Sequence: " + sequence);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        FibonacciGenerator generator = new FibonacciGenerator();

        System.out.print("Enter limit for Fibonacci sequence: ");
        int limit = sc.nextInt();

        List<Integer> sequence = generator.generateUpTo(limit);
        generator.displaySequence(sequence);

        sc.close();
    }
}