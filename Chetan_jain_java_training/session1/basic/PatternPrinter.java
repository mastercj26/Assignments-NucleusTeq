package Chetan_jain_java_training.session1.basic;

import java.util.Scanner;

public class PatternPrinter {

    private final char STAR = '*';
    private final char SPACE = ' ';

    private void printRightTriangle(int rows) {
        System.out.println("\nRight Triangle:");
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print(STAR + " ");
            }
            System.out.println();
        }
    }

    private void printInvertedTriangle(int rows) {
        System.out.println("\nInverted Triangle:");
        for (int i = rows; i >= 1; i--) {
            for (int j = 1; j <= i; j++) {
                System.out.print(STAR + " ");
            }
            System.out.println();
        }
    }

    private void printPyramid(int rows) {
        System.out.println("\nPyramid:");
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= rows - i; j++) {
                System.out.print(SPACE);
            }
            for (int k = 1; k <= (2 * i - 1); k++) {
                System.out.print(STAR);
            }
            System.out.println();
        }
    }

    private void printSquare(int size) {
        System.out.println("\nSquare:");
        for (int i = 1; i <= size; i++) {
            for (int j = 1; j <= size; j++) {
                System.out.print(STAR + " ");
            }
            System.out.println();
        }
    }

    private void printDiamond(int rows) {
        System.out.println("\nDiamond:");
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= rows - i; j++) {
                System.out.print(SPACE);
            }
            for (int k = 1; k <= (2 * i - 1); k++) {
                System.out.print(STAR);
            }
            System.out.println();
        }
        for (int i = rows - 1; i >= 1; i--) {
            for (int j = 1; j <= rows - i; j++) {
                System.out.print(SPACE);
            }
            for (int k = 1; k <= (2 * i - 1); k++) {
                System.out.print(STAR);
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        PatternPrinter printer = new PatternPrinter();

        System.out.print("Enter number of rows: ");
        int rows = sc.nextInt();

        printer.printRightTriangle(rows);
        printer.printInvertedTriangle(rows);
        printer.printPyramid(rows);
        printer.printSquare(rows);
        printer.printDiamond(rows);

        sc.close();
    }
}
