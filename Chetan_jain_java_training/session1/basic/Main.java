package Chetan_jain_java_training.session1.basic;
import java.util.Scanner;

public class Main {

    private final double PI = 3.14159265359;
    private Scanner sc = new Scanner(System.in);

    private void showMenu() {
        System.out.println("Select shape:");
        System.out.println("1. Circle");
        System.out.println("2. Rectangle");
        System.out.println("3. Triangle");
        System.out.print("Enter choice: ");
    }

    private void circleArea() {
        System.out.print("Enter radius: ");
        double r = sc.nextDouble();
        double area = PI * r * r;
        System.out.println("Area = " + area);
    }

    private void rectangleArea() {
        System.out.print("Enter length: ");
        double l = sc.nextDouble();
        System.out.print("Enter width: ");
        double w = sc.nextDouble();
        System.out.println("Area = " + (l * w));
    }

    private void triangleArea() {
        System.out.print("Enter base: ");
        double b = sc.nextDouble();
        System.out.print("Enter height: ");
        double h = sc.nextDouble();
        System.out.println("Area = " + (0.5 * b * h));
    }

    void run() {
        showMenu();
        int choice = sc.nextInt();

        if (choice == 1) {
            circleArea();
        } else if (choice == 2) {
            rectangleArea();
        } else if (choice == 3) {
            triangleArea();
        } else {
            System.out.println("Wrong input");
        }

        sc.close();
    }

    public static void main(String[] args) {
        Main m = new Main();
        m.run();
    }
}