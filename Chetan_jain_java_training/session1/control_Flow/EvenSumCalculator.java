package Chetan_jain_java_training.session1.control_Flow;



import java.util.Scanner;

public class EvenSumCalculator {

    public void printEvenAndSum(int start, int end) {

        int sum = 0;

        System.out.print("Even numbers: ");

        for (int i = start; i <= end; i++) {
            if (i % 2 == 0) {
                System.out.print(i + " ");
                sum += i;
            }
        }

        System.out.println("\nSum = " + sum);
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        EvenSumCalculator obj = new EvenSumCalculator();

        System.out.print("Enter start: ");
        int start = sc.nextInt();

        System.out.print("Enter end: ");
        int end = sc.nextInt();

        obj.printEvenAndSum(start, end);

        sc.close();
    }
}