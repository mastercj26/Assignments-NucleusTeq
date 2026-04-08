package Chetan_jain_java_training.session1.OOPS;

class Student {

    private String name;
    private int rollNo;
    private int marks;

    public void setDetails(String name, int rollNo, int marks) {
        this.name = name;
        this.rollNo = rollNo;
        this.marks = marks;
    }

    public void showDetails() {
        System.out.println("Name: " + name);
        System.out.println("Roll No: " + rollNo);
        System.out.println("Marks: " + marks);
    }

    public void display() {
        System.out.println("This is a Student");
    }

    public void display(String msg) {
        System.out.println(msg);
    }
}

class GraduateStudent extends Student {

    private String degree;

    public void setDegree(String degree) {
        this.degree = degree;
    }

    public void showGraduateDetails() {
        showDetails();
        System.out.println("Degree: " + degree);
    }

    public void display() {
        System.out.println("This is a Graduate Student");
    }
}

public class Main {
    public static void main(String[] args) {

        GraduateStudent obj = new GraduateStudent();

        obj.setDetails("Chetan", 101, 85);
        obj.setDegree("B.Tech");

        obj.showGraduateDetails();

        obj.display();
        obj.display("Method Overloading Example");
    }
}