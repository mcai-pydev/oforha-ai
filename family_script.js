// User Management
let currentUser = null;
let familyMembers = [];
let expenses = [];

// DOM Elements
const authSection = document.getElementById('auth-section');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const showRegisterLink = document.getElementById('show-register');
const showLoginLink = document.getElementById('show-login');
const registerBox = document.getElementById('register-box');
const logoutButton = document.getElementById('logout');
const mainSections = document.querySelectorAll('.main-section');
const profileName = document.getElementById('profile-name');
const userName = document.getElementById('user-name');

// Initialize year select
const yearSelect = document.getElementById('year-select');
const currentYear = new Date().getFullYear();
for (let year = currentYear - 5; year <= currentYear + 5; year++) {
    const option = document.createElement('option');
    option.value = year;
    option.textContent = year;
    if (year === currentYear) option.selected = true;
    yearSelect.appendChild(option);
}

// Event Listeners
showRegisterLink.addEventListener('click', (e) => {
    e.preventDefault();
    registerBox.style.display = 'block';
    registerBox.previousElementSibling.style.display = 'none';
});

showLoginLink.addEventListener('click', (e) => {
    e.preventDefault();
    registerBox.style.display = 'none';
    registerBox.previousElementSibling.style.display = 'block';
});

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    login(email, password);
});

registerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const role = document.getElementById('register-role').value;
    register(name, email, password, role);
});

logoutButton.addEventListener('click', (e) => {
    e.preventDefault();
    logout();
});

document.getElementById('expense-form').addEventListener('submit', (e) => {
    e.preventDefault();
    addExpense();
});

// User Authentication Functions
function login(email, password) {
    // In a real app, this would validate against a backend
    currentUser = {
        email: email,
        name: email.split('@')[0], // Simplified for demo
        role: 'parent'
    };
    updateUIAfterAuth();
}

function register(name, email, password, role) {
    // In a real app, this would send data to a backend
    currentUser = {
        name: name,
        email: email,
        role: role
    };
    updateUIAfterAuth();
}

function logout() {
    currentUser = null;
    updateUIAfterAuth();
}

// UI Update Functions
function updateUIAfterAuth() {
    if (currentUser) {
        authSection.style.display = 'none';
        mainSections.forEach(section => {
            if (section.id === 'dashboard') {
                section.style.display = 'block';
            }
        });
        logoutButton.style.display = 'inline-block';
        profileName.textContent = currentUser.name;
        userName.textContent = currentUser.name;
        loadDashboard();
    } else {
        authSection.style.display = 'block';
        mainSections.forEach(section => section.style.display = 'none');
        logoutButton.style.display = 'none';
    }
}

// Expense Management Functions
function addExpense() {
    const description = document.getElementById('expense-description').value;
    const amount = parseFloat(document.getElementById('expense-amount').value);
    const category = document.getElementById('expense-category').value;

    const expense = {
        id: Date.now(),
        description,
        amount,
        category,
        date: new Date(),
        userId: currentUser.email
    };

    expenses.push(expense);
    updateExpensesList();
    updateDashboard();
    document.getElementById('expense-form').reset();
}

function updateExpensesList() {
    const expensesList = document.getElementById('expenses-list');
    const userExpenses = expenses.filter(expense => expense.userId === currentUser.email);
    
    expensesList.innerHTML = userExpenses.map(expense => `
        <div class="expense-item" style="padding: 1rem; border-bottom: 1px solid #eee;">
            <h4 style="margin: 0;">${expense.description}</h4>
            <p style="margin: 0.5rem 0;">
                <span class="category" style="background: #eee; padding: 0.2rem 0.5rem; border-radius: 4px;">${expense.category}</span>
                <span class="amount" style="float: right;">$${expense.amount.toFixed(2)}</span>
            </p>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">${expense.date.toLocaleDateString()}</p>
        </div>
    `).join('');
}

function updateDashboard() {
    const personalSpending = document.getElementById('personal-spending');
    const familyTotal = document.getElementById('family-total');
    const budgetProgress = document.getElementById('budget-progress');

    const userExpenses = expenses.filter(expense => expense.userId === currentUser.email);
    const personalTotal = userExpenses.reduce((sum, expense) => sum + expense.amount, 0);
    const familyTotalAmount = expenses.reduce((sum, expense) => sum + expense.amount, 0);

    personalSpending.textContent = `$${personalTotal.toFixed(2)}`;
    familyTotal.textContent = `$${familyTotalAmount.toFixed(2)}`;

    // Assuming a monthly budget of $1000 for demonstration
    const budget = 1000;
    const progressPercentage = Math.min((personalTotal / budget) * 100, 100);
    budgetProgress.style.width = `${progressPercentage}%`;
    budgetProgress.style.backgroundColor = progressPercentage > 90 ? '#e74c3c' : '#27ae60';
}

function loadDashboard() {
    updateExpensesList();
    updateDashboard();
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    // Set up navigation
    document.querySelectorAll('.topmenu').forEach(link => {
        link.addEventListener('click', (e) => {
            if (!currentUser && e.target.id !== 'logout') {
                e.preventDefault();
                return;
            }
            
            const targetId = e.target.getAttribute('href').substring(1);
            if (targetId && targetId !== '#') {
                mainSections.forEach(section => {
                    section.style.display = section.id === targetId ? 'block' : 'none';
                });
            }
        });
    });
}); 