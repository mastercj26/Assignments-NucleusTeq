package Chetan_jain_java_training.session1.control_Flow;



import java.util.Scanner;

public class MultiplicationTable {

    public void printTable(int num, int range) {

        System.out.println("Multiplication Table of " + num);

        for (int i = 1; i <= range; i++) {
            System.out.println(num + " x " + i + " = " + (num * i));
        }
    }

    public void printGrid(int size) {

        System.out.println("\nMultiplication Grid:");

        for (int i = 1; i <= size; i++) {
            for (int j = 1; j <= size; j++) {
                System.out.print((i * j) + "\t");
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        MultiplicationTable obj = new MultiplicationTable();

        System.out.print("Enter a number: ");
        int num = sc.nextInt();

        System.out.print("Enter range: ");
        int range = sc.nextInt();

        obj.printTable(num, range);

        System.out.print("\nEnter grid size: ");
        int size = sc.nextInt();

        obj.printGrid(size);

        sc.close();
    }
}