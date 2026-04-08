package Chetan_jain_java_training.session1.array;



import java.util.Scanner;

public class ArrayAverageCalculator {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of elements: ");
        int n = sc.nextInt();

        int[] arr = new int[n];

        System.out.println("Enter elements:");

        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        int sum = 0;
        int min = arr[0];
        int max = arr[0];

        for (int i = 0; i < n; i++) {
            sum += arr[i];

            if (arr[i] < min) {
                min = arr[i];
            }

            if (arr[i] > max) {
                max = arr[i];
            }
        }

        double avg = (double) sum / n;

        System.out.print("Array: ");
        for (int i = 0; i < n; i++) {
            System.out.print(arr[i] + " ");
        }

        System.out.println("\nSum = " + sum);
        System.out.println("Average = " + avg);
        System.out.println("Minimum = " + min);
        System.out.println("Maximum = " + max);

        sc.close();
    }
}
