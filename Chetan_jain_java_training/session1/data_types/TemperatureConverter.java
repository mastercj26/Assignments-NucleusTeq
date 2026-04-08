package Chetan_jain_java_training.session1.data_types;

import java.util.Scanner;

public class TemperatureConverter {

    public double celsiusToFahrenheit(double celsius) {
        return (celsius * 9 / 5) + 32;
    }

    public double fahrenheitToCelsius(double fahrenheit) {
        return (fahrenheit - 32) * 5 / 9;
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        TemperatureConverter obj = new TemperatureConverter();

        System.out.println("=== Temperature Converter ===");
        System.out.println("1. Celsius to Fahrenheit");
        System.out.println("2. Fahrenheit to Celsius");
        System.out.print("Enter your choice: ");

        int choice = sc.nextInt();

        if (choice == 1) {
            System.out.print("Enter temperature in Celsius: ");
            double c = sc.nextDouble();

            double f = obj.celsiusToFahrenheit(c);
            System.out.println("Result: " + c + "°C = " + f + "°F");

        } else if (choice == 2) {
            System.out.print("Enter temperature in Fahrenheit: ");
            double f = sc.nextDouble();

            double c = obj.fahrenheitToCelsius(f);
            System.out.println("Result: " + f + "°F = " + c + "°C");

        } else {
            System.out.println("Invalid choice!");
        }

        sc.close();
    }
}