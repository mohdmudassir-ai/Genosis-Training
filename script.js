const API_BASE_URL = 'https://ginosis-production.up.railway.app'; // Make sure this matches your FastAPI server

const studentForm = document.getElementById('student-form');
const studentsTbody = document.getElementById('students-tbody');
const formTitle = document.getElementById('form-title');
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toast-message');

let isEditing = false;
let currentEditName = '';

// Initialize
document.addEventListener('DOMContentLoaded', fetchStudents);

// Handle Form Submission
studentForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const course = document.getElementById('course').value;
    const marks = document.getElementById('marks').value;

    if (isEditing) {
        await updateStudent(currentEditName, course, marks);
    } else {
        await createStudent(name, course, marks);
    }
});

// Handle Cancel Edit
cancelBtn.addEventListener('click', resetForm);

// Fetch all students
async function fetchStudents() {
    try {
        const response = await fetch(`${API_BASE_URL}/students`);
        if (!response.ok) throw new Error('Failed to fetch students');
        
        const result = await response.json();
        renderStudents(result.data || []);
    } catch (error) {
        console.error(error);
        showToast('Failed to load students from server. Is the backend running?', 'error');
        studentsTbody.innerHTML = '<tr><td colspan="4" class="text-center loading-text" style="color: var(--danger-color)">Error loading data.</td></tr>';
    }
}

// Render students in table
function renderStudents(students) {
    if (students.length === 0) {
        studentsTbody.innerHTML = '<tr><td colspan="4" class="text-center loading-text">No students found. Add one!</td></tr>';
        return;
    }

    studentsTbody.innerHTML = '';
    
    students.forEach(student => {
        const tr = document.createElement('tr');
        
        tr.innerHTML = `
            <td><strong>${escapeHTML(student.name)}</strong></td>
            <td>${escapeHTML(student.course)}</td>
            <td>${student.marks}</td>
            <td class="actions-cell">
                <button class="btn btn-edit" onclick="editStudent('${escapeHTML(student.name)}', '${escapeHTML(student.course)}', ${student.marks})">Edit</button>
                <button class="btn btn-danger" onclick="deleteStudent('${escapeHTML(student.name)}')">Delete</button>
            </td>
        `;
        
        studentsTbody.appendChild(tr);
    });
}

// Create new student
async function createStudent(name, course, marks) {
    try {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Adding...';

        // FastAPI endpoints in sample.py expect these as query parameters
        const url = new URL(`${API_BASE_URL}/students`);
        url.searchParams.append('name', name);
        url.searchParams.append('course', course);
        url.searchParams.append('marks', marks);

        const response = await fetch(url, { method: 'POST' });
        
        if (!response.ok) throw new Error('Failed to create student');
        
        showToast('Student added successfully!', 'success');
        resetForm();
        fetchStudents();
    } catch (error) {
        console.error(error);
        showToast('Error creating student', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Add Student';
    }
}

// Prepare edit mode
window.editStudent = function(name, course, marks) {
    isEditing = true;
    currentEditName = name;
    
    document.getElementById('name').value = name;
    document.getElementById('name').disabled = true; // Name shouldn't change as it's the identifier
    document.getElementById('course').value = course;
    document.getElementById('marks').value = marks;
    
    formTitle.textContent = 'Edit Student';
    submitBtn.textContent = 'Update Student';
    cancelBtn.classList.remove('hidden');
    
    // Scroll to form smoothly
    document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
}

// Update student
async function updateStudent(name, course, marks) {
    try {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Updating...';

        const url = new URL(`${API_BASE_URL}/students/${encodeURIComponent(name)}`);
        url.searchParams.append('course', course);
        url.searchParams.append('marks', marks);

        const response = await fetch(url, { method: 'PUT' });
        
        if (!response.ok) throw new Error('Failed to update student');
        
        showToast('Student updated successfully!', 'success');
        resetForm();
        fetchStudents();
    } catch (error) {
        console.error(error);
        showToast('Error updating student', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Add Student'; // Will be reset properly by resetForm
    }
}

// Delete student
window.deleteStudent = async function(name) {
    if (!confirm(`Are you sure you want to delete ${name}?`)) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/students/${encodeURIComponent(name)}`, { 
            method: 'DELETE' 
        });
        
        if (!response.ok) throw new Error('Failed to delete student');
        
        showToast('Student deleted successfully!', 'success');
        
        if (isEditing && currentEditName === name) {
            resetForm();
        }
        
        fetchStudents();
    } catch (error) {
        console.error(error);
        showToast('Error deleting student', 'error');
    }
}

// Reset form state
function resetForm() {
    studentForm.reset();
    isEditing = false;
    currentEditName = '';
    
    document.getElementById('name').disabled = false;
    formTitle.textContent = 'Add New Student';
    submitBtn.textContent = 'Add Student';
    cancelBtn.classList.add('hidden');
}

// Toast notification
let toastTimeout;
function showToast(message, type = 'success') {
    toastMessage.textContent = message;
    
    toast.className = 'toast show';
    if (type === 'success') {
        toast.classList.add('success');
    } else {
        toast.classList.add('error');
    }
    
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Simple HTML escaping to prevent XSS
function escapeHTML(str) {
    if (!str) return '';
    return str.toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}