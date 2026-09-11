// Railway FastAPI backend
const API_URL = "https://genosis-training-production.up.railway.app";

// ===============================
// API STATUS
// ===============================

async function checkBackend() {
    const status = document.getElementById("backendStatus");

    try {
        const response = await fetch(`${API_URL}/health`);

        if (response.ok) {
            status.textContent = "Backend Online";
            status.className = "status online";
        } else {
            throw new Error("Backend error");
        }
    } catch (error) {
        status.textContent = "Backend Offline";
        status.className = "status offline";
    }
}


// ===============================
// LOAD STUDENTS
// ===============================

async function loadStudents() {
    try {
        const response = await fetch(`${API_URL}/students`);

        if (!response.ok) {
            throw new Error("Failed to load students");
        }

        const students = await response.json();

        const tableBody = document.getElementById("studentTableBody");

        if (!tableBody) return;

        tableBody.innerHTML = "";

        students.forEach(student => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${escapeHtml(student.name)}</td>
                <td>${escapeHtml(student.email)}</td>
                <td>${student.age}</td>
                <td>${student.marks}</td>
            `;

            tableBody.appendChild(row);
        });

        updateDashboard(students);

    } catch (error) {
        console.error(error);
    }
}


// ===============================
// DASHBOARD
// ===============================

function updateDashboard(students) {

    const totalStudents = document.getElementById("totalStudents");
    const averageMarks = document.getElementById("averageMarks");
    const highestMarks = document.getElementById("highestMarks");

    if (!students.length) {
        if (totalStudents) totalStudents.textContent = "0";
        if (averageMarks) averageMarks.textContent = "0";
        if (highestMarks) highestMarks.textContent = "0";
        return;
    }

    const total = students.length;

    const marks = students.map(student =>
        Number(student.marks) || 0
    );

    const average =
        marks.reduce((sum, mark) => sum + mark, 0) / marks.length;

    const highest = Math.max(...marks);

    if (totalStudents)
        totalStudents.textContent = total;

    if (averageMarks)
        averageMarks.textContent = average.toFixed(2);

    if (highestMarks)
        highestMarks.textContent = highest;
}


// ===============================
// ADD STUDENT
// ===============================

async function addStudent(event) {

    event.preventDefault();

    const name = document.getElementById("addName").value;
    const email = document.getElementById("addEmail").value;
    const age = document.getElementById("addAge").value;
    const marks = document.getElementById("addMarks").value;

    const message = document.getElementById("addMessage");

    try {

        const response = await fetch(
            `${API_URL}/students?name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&age=${age}&marks=${marks}`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to add student");
        }

        showMessage(message, "Student added successfully!", "success");

        document.getElementById("addForm").reset();

        loadStudents();

    } catch (error) {

        showMessage(message, error.message, "error");

    }
}


// ===============================
// UPDATE STUDENT
// ===============================

async function updateStudent(event) {

    event.preventDefault();

    const id = document.getElementById("updateId").value;
    const name = document.getElementById("updateName").value;
    const email = document.getElementById("updateEmail").value;
    const age = document.getElementById("updateAge").value;
    const marks = document.getElementById("updateMarks").value;

    const message = document.getElementById("updateMessage");

    try {

        const response = await fetch(
            `${API_URL}/students/${id}?name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&age=${age}&marks=${marks}`,
            {
                method: "PUT"
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to update student");
        }

        showMessage(message, "Student updated successfully!", "success");

        document.getElementById("updateForm").reset();

        loadStudents();

    } catch (error) {

        showMessage(message, error.message, "error");

    }
}


// ===============================
// DELETE STUDENT
// ===============================

async function deleteStudent(event) {

    event.preventDefault();

    const id = document.getElementById("deleteId").value;

    const message = document.getElementById("deleteMessage");

    try {

        const response = await fetch(
            `${API_URL}/students/${id}`,
            {
                method: "DELETE"
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to delete student");
        }

        showMessage(message, "Student deleted successfully!", "success");

        document.getElementById("deleteForm").reset();

        loadStudents();

    } catch (error) {

        showMessage(message, error.message, "error");

    }
}


// ===============================
// MESSAGE
// ===============================

function showMessage(element, text, type) {

    if (!element) return;

    element.textContent = text;

    element.className = `message ${type}`;

    element.style.display = "block";

    setTimeout(() => {
        element.style.display = "none";
    }, 3000);
}


// ===============================
// SECURITY
// ===============================

function escapeHtml(value) {

    const div = document.createElement("div");

    div.textContent = value ?? "";

    return div.innerHTML;
}


// ===============================
// NAVIGATION
// ===============================

function showSection(sectionId) {

    document.querySelectorAll(".section").forEach(section => {
        section.style.display = "none";
    });

    const section = document.getElementById(sectionId);

    if (section) {
        section.style.display = "block";
    }

    document.querySelectorAll(".nav-link").forEach(link => {
        link.classList.remove("active");
    });
}


// ===============================
// START APP
// ===============================

document.addEventListener("DOMContentLoaded", () => {

    checkBackend();

    loadStudents();

    const addForm = document.getElementById("addForm");
    const updateForm = document.getElementById("updateForm");
    const deleteForm = document.getElementById("deleteForm");

    if (addForm) {
        addForm.addEventListener("submit", addStudent);
    }

    if (updateForm) {
        updateForm.addEventListener("submit", updateStudent);
    }

    if (deleteForm) {
        deleteForm.addEventListener("submit", deleteStudent);
    }

});