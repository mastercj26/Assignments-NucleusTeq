package Chetan_jain_java_training.session1.data_types;



public class OperatorDemo {

    private void arithmeticOperators() {
        

        int a = 15;
        int b = 4;

        System.out.println("a = " + a + ", b = " + b);
        System.out.println("Addition (a + b): " + (a + b));
        System.out.println("Subtraction (a - b): " + (a - b));
        System.out.println("Multiplication (a * b): " + (a * b));
        System.out.println("Division (a / b): " + (a / b));
        System.out.println("Modulus (a % b): " + (a % b));

        int x = 10;
        System.out.println("\nOriginal x: " + x);
        System.out.println("Post-increment (x++): " + (x++));
        System.out.println("After post-increment: " + x);
        System.out.println("Pre-increment (++x): " + (++x));
        System.out.println("Post-decrement (x--): " + (x--));
        System.out.println("Pre-decrement (--x): " + (--x));
    }

    private void relationalOperators() {
        

        int num1 = 10;
        int num2 = 20;

        System.out.println("num1 = " + num1 + ", num2 = " + num2);
        System.out.println("Equal to (num1 == num2): " + (num1 == num2));
        System.out.println("Not equal to (num1 != num2): " + (num1 != num2));
        System.out.println("Greater than (num1 > num2): " + (num1 > num2));
        System.out.println("Less than (num1 < num2): " + (num1 < num2));
        System.out.println("Greater than or equal (num1 >= num2): " + (num1 >= num2));
        System.out.println("Less than or equal (num1 <= num2): " + (num1 <= num2));
    }

    private void logicalOperators() {
      

        boolean condition1 = true;
        boolean condition2 = false;

        System.out.println("condition1 = " + condition1 + ", condition2 = " + condition2);
        System.out.println("Logical AND (condition1 && condition2): " + (condition1 && condition2));
        System.out.println("Logical OR (condition1 || condition2): " + (condition1 || condition2));
        System.out.println("Logical NOT (!condition1): " + (!condition1));

        int a = 10;
        int b = 0;
        System.out.println("\nShort-circuit AND: " + (b != 0 && a / b > 0));
        System.out.println("Short-circuit OR: " + (b == 0 || a / b > 0));
    }

    private void bitwiseOperators() {
        

        int x = 5;
        int y = 3;

        System.out.println("x = " + x + " (binary: 0101)");
        System.out.println("y = " + y + " (binary: 0011)");
        System.out.println("Bitwise AND (x & y): " + (x & y) + " (binary: 0001)");
        System.out.println("Bitwise OR (x | y): " + (x | y) + " (binary: 0111)");
        System.out.println("Bitwise XOR (x ^ y): " + (x ^ y) + " (binary: 0110)");
        System.out.println("Bitwise Complement (~x): " + (~x));
        System.out.println("Left Shift (x << 1): " + (x << 1) + " (binary: 1010)");
        System.out.println("Right Shift (x >> 1): " + (x >> 1) + " (binary: 0010)");
    }

    private void assignmentOperators() {
        

        int num = 10;
        System.out.println("Initial value: " + num);

        num += 5;
        System.out.println("After += 5: " + num);

        num -= 3;
        System.out.println("After -= 3: " + num);

        num *= 2;
        System.out.println("After *= 2: " + num);

        num /= 4;
        System.out.println("After /= 4: " + num);

        num %= 3;
        System.out.println("After %= 3: " + num);
    }

    private void ternaryOperator() {
        

        int age = 20;
        String result = (age >= 18) ? "Adult" : "Minor";
        System.out.println("Age: " + age + " -> " + result);

        int a = 10, b = 20;
        int max = (a > b) ? a : b;
        System.out.println("Maximum of " + a + " and " + b + ": " + max);
    }

    public static void main(String[] args) {
        OperatorDemo demo = new OperatorDemo();
        demo.arithmeticOperators();
        demo.relationalOperators();
        demo.logicalOperators();
        demo.bitwiseOperators();
        demo.assignmentOperators();
        demo.ternaryOperator();
    }
}