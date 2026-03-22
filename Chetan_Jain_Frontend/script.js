
const students = [
    {
        name: "Chetan",
        marks: [
            { subject: "Math", score: 78 },
            { subject: "English", score: 82 },
            { subject: "Science", score: 74 },
            { subject: "History", score: 69 },
            { subject: "Computer", score: 88 }
        ],
        attendance: 82
    },
    {
        name: "Rahul",
        marks: [
            { subject: "Math", score: 90 },
            { subject: "English", score: 85 },
            { subject: "Science", score: 80 },
            { subject: "History", score: 76 },
            { subject: "Computer", score: 92 }
        ],
        attendance: 91
    },
    {
        name: "Aman",
        marks: [
            { subject: "Math", score: 55 },
            { subject: "English", score: 60 },
            { subject: "Science", score: 58 },
            { subject: "History", score: 52 },
            { subject: "Computer", score: 65 }
        ],
        
        attendance: 68
    },
    {
        name: "Riya",
        marks: [
            { subject: "Math", score: 88 },
            { subject: "English", score: 76 },
            // 38 is below 40, this should cause a subject fail
            { subject: "Science", score: 38 },
            { subject: "History", score: 71 },
            { subject: "Computer", score: 84 }
        ],
        attendance: 87
    },
    {
        name: "Sneha",
        marks: [
            { subject: "Math", score: 95 },
            { subject: "English", score: 89 },
            { subject: "Science", score: 91 },
            { subject: "History", score: 85 },
            { subject: "Computer", score: 97 }
        ],
        attendance: 96
    }
];


function calculateTotalMarks(student) {
    let total = 0;
    student.marks.forEach(function(markObj) {
        total = total + markObj.score;
    });
    return total;
}


function calculateAverage(student) {
    let total = calculateTotalMarks(student);
    let numberOfSubjects = student.marks.length;
    let average = total / numberOfSubjects;
    return parseFloat(average.toFixed(1));
}


function getAllSubjects() {
    let subjects = [];
    for (let j = 0; j < students[0].marks.length; j++) {
        subjects.push(students[0].marks[j].subject);
    }
    return subjects;
}


function findSubjectWiseHighest() {
    let subjects = getAllSubjects();

    console.log("\n===== SUBJECT-WISE HIGHEST SCORE =====");

    for (let s = 0; s < subjects.length; s++) {
        let currentSubject = subjects[s];
        let highestScore = -1;
        let topperName = "";

        for (let i = 0; i < students.length; i++) {
            for (let m = 0; m < students[i].marks.length; m++) {
                if (students[i].marks[m].subject === currentSubject) {
                    if (students[i].marks[m].score > highestScore) {
                        highestScore = students[i].marks[m].score;
                        topperName = students[i].name;
                    }
                }
            }
        }

        console.log("Highest in " + currentSubject + ": " + topperName + " (" + highestScore + ")");
    }
}



function findSubjectWiseAverage() {
    let subjects = getAllSubjects();

    console.log("\n SUBJECT-WISE AVERAGE SCORE ");

    for (let s = 0; s < subjects.length; s++) {
        let currentSubject = subjects[s];
        let totalForSubject = 0;
        let studentCount = 0;

        for (let i = 0; i < students.length; i++) {
            for (let m = 0; m < students[i].marks.length; m++) {
                if (students[i].marks[m].subject === currentSubject) {
                    totalForSubject = totalForSubject + students[i].marks[m].score;
                    studentCount++;
                }
            }
        }

        let subjectAvg = totalForSubject / studentCount;
        console.log("Average " + currentSubject + " Score: " + parseFloat(subjectAvg.toFixed(1)));
    }
}



function findClassTopper() {
    let topperName = "";
    let topperMarks = 0;

    for (let i = 0; i < students.length; i++) {
        let currentTotal = calculateTotalMarks(students[i]);
        if (currentTotal > topperMarks) {
            topperMarks = currentTotal;
            topperName = students[i].name;
        }
    }

    console.log("Class Topper: " + topperName + " with " + topperMarks + " marks");
}

function checkFailedSubject(student) {
    for (let m = 0; m < student.marks.length; m++) {
        if (student.marks[m].score <= 40) {
            return student.marks[m].subject;
        }
    }
    return null;
}


function assignGrade(student) {
    let average = calculateAverage(student);

    // fail check 1: attendance below 75
    if (student.attendance < 75) {
        return "Fail (Low Attendance)";
    }

    // fail check 2: any subject score 40 or below
    let failedSubject = checkFailedSubject(student);
    if (failedSubject !== null) {
        return "Fail (Failed in " + failedSubject + ")";
    }

    
    if (average >= 85) {
        return "A";
    } else if (average >= 70) {
        return "B";
    } else if (average >= 50) {
        return "C";
    } else {
        return "Fail";
    }
}


console.log("   STUDENT PERFORMANCE ANALYZER");

console.log("Total Students Loaded: " + students.length);

// 1. Total Marks
console.log("\n TOTAL MARKS ");
for (let i = 0; i < students.length; i++) {
    let total = calculateTotalMarks(students[i]);
    console.log(students[i].name + " Total Marks: " + total);
}

// 2. Average Marks
console.log("\n AVERAGE MARKS ");
for (let i = 0; i < students.length; i++) {
    let avg = calculateAverage(students[i]);
    console.log(students[i].name + " Average: " + avg);
}

// 3. Subject-wise Highest
findSubjectWiseHighest();

// 4. Subject-wise Average
findSubjectWiseAverage();

// 5. Class Topper
findClassTopper();

// 6. Grades
console.log("\n STUDENT GRADES ");
for (let i = 0; i < students.length; i++) {
    let grade = assignGrade(students[i]);
    console.log(students[i].name + " Grade: " + grade);
}




console.log("\nCOMPLETE SUMMARY ");

for (let i = 0; i < students.length; i++) {
    let total = calculateTotalMarks(students[i]);
    let avg = calculateAverage(students[i]);
    let grade = assignGrade(students[i]);

    console.log("Name: " + students[i].name);
    console.log(+ total + "  Average: " + avg + " Attendance: " + students[i].attendance + "%");
    console.log( grade);
  
}

c