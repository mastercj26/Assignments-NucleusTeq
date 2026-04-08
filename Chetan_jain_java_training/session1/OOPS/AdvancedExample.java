package Chetan_jain_java_training.session1.OOPS;

import java.io.*;
import java.util.Scanner;

interface Animal {
    void sound();
}

abstract class Vehicle {
    abstract void start();

    void stop() {
        System.out.println("Vehicle stopped");
    }
}

class Dog implements Animal {
    public void sound() {
        System.out.println("Dog barks");
    }
}

class Car extends Vehicle {
    void start() {
        System.out.println("Car starts");
    }
}

class MyThread extends Thread {
    public void run() {
        for (int i = 1; i <= 5; i++) {
            System.out.println("Thread running: " + i);
        }
    }
}

public class AdvancedExample {

    public static void main(String[] args) {

        Dog d = new Dog();
        d.sound();

        Car c = new Car();
        c.start();
        c.stop();

        try {
            int a = 10;
            int b = 0;
            int result = a / b;
            System.out.println(result);
        } catch (Exception e) {
            System.out.println("Exception handled: " + e);
        }

        try {
            BufferedReader br = new BufferedReader(new FileReader("test.txt"));
            String line;

            System.out.println("File content:");
            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }

            br.close();
        } catch (Exception e) {
            System.out.println("File error: " + e);
        }

        MyThread t1 = new MyThread();
        t1.start();

        System.out.println("Main method ends");
    }
}