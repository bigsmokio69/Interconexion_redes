function showDetails(position, name) {
    document.getElementById('worker-position').innerText = position;
    document.getElementById('worker-name').innerText = name;
    document.getElementById('worker-matricula').innerText = '12345'; // Aquí puedes añadir los datos correspondientes
    document.getElementById('worker-email').innerText = 'correo@example.com'; // Aquí puedes añadir los datos correspondientes
    document.getElementById('worker-phone').innerText = '123-456-7890'; // Aquí puedes añadir los datos correspondientes
    document.getElementById('profile-picture').src = 'profile1.jpg'; // Cambia la fuente de la imagen de perfil según el trabajador
}

function toggleFilterMenu() {
    var filterMenu = document.getElementById('filter-menu');
    if (filterMenu.style.display === 'block') {
        filterMenu.style.display = 'none';
    } else {
        filterMenu.style.display = 'block';
    }
}

function applyFilter() {
    var checkboxes = document.querySelectorAll('input[name="worker-type"]:checked');
    var selectedTypes = Array.from(checkboxes).map(cb => cb.value);

    var workers = document.querySelectorAll('.worker');
    workers.forEach(worker => {
        if (selectedTypes.length === 0 || selectedTypes.includes(worker.getAttribute('data-type'))) {
            worker.style.display = 'block';
        } else {
            worker.style.display = 'none';
        }
    });
}

function clearFilter() {
    var checkboxes = document.querySelectorAll('input[name="worker-type"]');
    checkboxes.forEach(cb => cb.checked = false);
    applyFilter();
}


