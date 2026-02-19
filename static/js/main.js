/**
 * Library Management System - JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });

    // Confirm delete actions
    const deleteLinks = document.querySelectorAll('.btn-delete');
    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('.data-form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = 'red';
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Table row hover effect
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('click', function(e) {
            if (!e.target.closest('.btn-icon') && !e.target.closest('a')) {
                // Optional: Add row selection logic here
            }
        });
    });

    // Search input auto-focus
    const searchInput = document.querySelector('.search-form input[type="text"]');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const form = searchInput.closest('form');
                if (form) {
                    form.submit();
                }
            }
        });
    }

    // Date formatting
    const dateElements = document.querySelectorAll('.date-format');
    dateElements.forEach(function(element) {
        const date = new Date(element.textContent);
        element.textContent = date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    });

    // Number input validation
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            if (this.value < this.min) {
                this.value = this.min;
            }
            if (this.max && this.value > this.max) {
                this.value = this.max;
            }
        });
    });

    // Loading state for forms
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            if (this.form && !this.classList.contains('no-loading')) {
                this.disabled = true;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                setTimeout(() => {
                    this.form.submit();
                }, 100);
            }
        });
    });

    // Table sort functionality
    const sortableHeaders = document.querySelectorAll('.data-table th[data-sort]');
    sortableHeaders.forEach(function(header) {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const table = header.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const columnIndex = Array.from(header.parentNode.children).indexOf(header);
            const isAscending = header.classList.toggle('asc');
            
            rows.sort(function(a, b) {
                const aText = a.children[columnIndex].textContent.trim();
                const bText = b.children[columnIndex].textContent.trim();
                
                if (isAscending) {
                    return aText.localeCompare(bText);
                } else {
                    return bText.localeCompare(aText);
                }
            });
            
            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
            
            // Update sort indicators
            sortableHeaders.forEach(function(h) {
                h.classList.remove('asc', 'desc');
            });
            header.classList.add(isAscending ? 'asc' : 'desc');
        });
    });

    console.log('Library Management System initialized');
});
