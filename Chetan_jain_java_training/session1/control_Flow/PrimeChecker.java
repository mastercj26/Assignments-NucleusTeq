package Chetan_jain_java_training.session1.control_Flow;


import java.util.Scanner;

public class PrimeChecker {

    public boolean isPrime(int n) {

        if (n <= 1) {
            return false;
        }

        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) {
                return false;
            }
        }

        return true;
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        PrimeChecker obj = new PrimeChecker();

        System.out.print("Enter a number: ");
        int num = sc.nextInt();

        if (obj.isPrime(num)) {
            System.out.println(num + " is a Prime number");
        } else {
            System.out.println(num + " is NOT a Prime number");

            if (num > 1) {
                System.out.print("Factors: ");
                for (int i = 1; i <= num; i++) {
                    if (num % i == 0) {
                        System.out.print(i + " ");
                    }
                }
                System.out.println();
            }
        }

        sc.close();
    }
}