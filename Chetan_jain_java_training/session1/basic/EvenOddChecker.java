package Chetan_jain_java_training.session1.basic;
import java.util.Scanner;
public class EvenOddChecker   {
   


    private final int DIVISOR = 2;

    private boolean isEven(int number) {
        return number % DIVISOR == 0;
    }

    private boolean isOdd(int number) {
        return !isEven(number);
    }

    private void checkAndDisplay(int number) {
        if (isEven(number)) {
            System.out.println(number + " is EVEN");
        } else {
            System.out.println(number + " is ODD");
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        EvenOddChecker checker = new EvenOddChecker();

        System.out.print("Enter a number: ");
        int num = sc.nextInt();

        checker.checkAndDisplay(num);

        sc.close();
    }
}

