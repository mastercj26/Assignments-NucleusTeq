package Chetan_jain_java_training.session1.basic;


import java.util.Scanner;

public class FactorialCalculator {

    private final int MIN_VALUE = 0;
    private final int MAX_VALUE = 20;

    private void validateInput(int number) {
        if (number < MIN_VALUE) {
            throw new IllegalArgumentException("Number must be non-negative");
        }
        if (number > MAX_VALUE) {
            throw new IllegalArgumentException("Number too large (max 20)");
        }
    }

    private long calculateIterative(int number) {
        validateInput(number);

        if (number == 0 || number == 1) {
            return 1;
        }

        long result = 1;
        for (int i = 2; i <= number; i++) {
            result *= i;
        }

        return result;
    }

    private long calculateRecursive(int number) {
        validateInput(number);

        if (number == 0 || number == 1) {
            return 1;
        }

        return number * calculateRecursive(number - 1);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        FactorialCalculator calculator = new FactorialCalculator();

        System.out.print("Enter a number: ");
        int num = sc.nextInt();

        try {
            long iterativeResult = calculator.calculateIterative(num);
            long recursiveResult = calculator.calculateRecursive(num);

            System.out.println("Factorial (Iterative): " + iterativeResult);
            System.out.println("Factorial (Recursive): " + recursiveResult);
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }

        sc.close();
    }
}