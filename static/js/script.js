function filterByPriority(priority) {
    const reports = document.querySelectorAll('.report-container .report');
    reports.forEach(report => {
        if (priority === 'all' || report.dataset.priority === priority) {
            report.closest('.report-container').style.display = '';
        } else {
            report.closest('.report-container').style.display = 'none';
        }
    });
}

function sortByDate(order) {
    const reports = Array.from(document.querySelectorAll('.report-container'));
    reports.sort((a, b) => {
        const dateA = new Date(a.querySelector('.report').dataset.date);
        const dateB = new Date(b.querySelector('.report').dataset.date);
        return order === 'recent' ? dateB - dateA : dateA - dateB;
    });
    const container = document.getElementById('reports');
    reports.forEach(report => container.appendChild(report));
}

function filterBySpecificDate() {
    const dateInput = document.getElementById('specific-date').value;
    const selectedDate = new Date(dateInput);
    const reports = document.querySelectorAll('.report-container .report');
    reports.forEach(report => {
        const reportDate = new Date(report.dataset.date);
        if (selectedDate.getTime() === reportDate.getTime()) {
            report.closest('.report-container').style.display = '';
        } else {
            report.closest('.report-container').style.display = 'none';
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    function assignPriority(button, priority) {
        const report = button.closest('.report');
        const priorityButtons = report.querySelector('.priority-buttons-bottom');
        const reportId = report.dataset.id;

        // Remove priority buttons
        priorityButtons.remove();

        // Change report color based on priority
        report.classList.remove('unassigned', 'normal', 'intermedia', 'urgente');
        report.dataset.priority = priority;
        if (priority === 'normal') {
            report.classList.add('normal');
            report.style.borderColor = 'green';
        } else if (priority === 'intermedia') {
            report.classList.add('intermedia');
            report.style.borderColor = 'orange';
        } else if (priority === 'urgente') {
            report.classList.add('urgente');
            report.style.borderColor = 'red';
        }

        // Send AJAX request to update priority in the database
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/asignar_prioridad', true);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.onload = function() {};
        xhr.send(JSON.stringify({
            report_id: reportId,
            priority: priority
        }));
    }

    // Event listeners for priority buttons
    document.querySelectorAll('.priority-button').forEach(function(button) {
        button.addEventListener('click', function() {
            const priority = this.name; // Assuming name is 'normal', 'intermediate', or 'urgent'
            assignPriority(this, priority);
        });
    });
});






function showAllReports() {
    const reports = document.querySelectorAll('.report-container .report');
    reports.forEach(report => {
        report.closest('.report-container').style.display = '';
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const detailButtons = document.querySelectorAll('.details-button button');

    detailButtons.forEach(button => {
        button.addEventListener('click', () => {
            const report = button.closest('.report');
            const description = report.querySelector('.report-description');
            
            if (report.classList.contains('expanded')) {
                // Colapsar la tarjeta
                report.classList.remove('expanded');
                description.classList.remove('full');
                description.classList.add('preview');
                button.textContent = 'Detalles';
            } else {
                // Expandir la tarjeta
                report.classList.add('expanded');
                description.classList.remove('preview');
                description.classList.add('full');
                button.textContent = 'Ocultar detalles';
            }
        });
    });
});


