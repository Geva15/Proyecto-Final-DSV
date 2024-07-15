document.getElementById('switchMode').addEventListener('click', () => {
    window.location.href = 'inicio_vista.html';
});

// JavaScript para manejar CRUD
document.addEventListener('DOMContentLoaded', () => {
    const adminList = document.getElementById('adminList');
    const crudModal = document.getElementById('crudModal');
    const modalTitle = document.getElementById('modalTitle');
    const crudForm = document.getElementById('crudForm');
    const adminIdInput = document.getElementById('adminId');
    const adminNameInput = document.getElementById('adminName');
    const adminEmailInput = document.getElementById('adminEmail');
    const cancelButton = document.getElementById('cancelButton');
    const addAdminButton = document.getElementById('addAdmin');

    let admins = [
        { id: 1, name: 'Juan Pérez', email: 'juan.perez@example.com' },
        { id: 2, name: 'María López', email: 'maria.lopez@example.com' },
        { id: 3, name: 'Carlos Sánchez', email: 'carlos.sanchez@example.com' },
    ];
    let editingAdminIndex = null;

    function renderAdmins() {
        adminList.innerHTML = '';
        admins.forEach((admin, index) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="py-2">${admin.id}</td>
                <td class="py-2">${admin.name}</td>
                <td class="py-2">${admin.email}</td>
                <td class="py-2">
                    <button class="bg-green-500 text-white px-2 py-1 rounded hover:bg-green-700" onclick="editAdmin(${index})">Editar</button>
                    <button class="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-700" onclick="deleteAdmin(${index})">Eliminar</button>
                </td>
            `;
            adminList.appendChild(tr);
        });
    }

    function openModal(title) {
        modalTitle.textContent = title;
        crudModal.classList.remove('hidden');
    }

    function closeModal() {
        crudModal.classList.add('hidden');
        crudForm.reset();
        editingAdminIndex = null;
    }

    addAdminButton.addEventListener('click', () => {
        openModal('Agregar Administrativo');
    });

    cancelButton.addEventListener('click', closeModal);

    crudForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const adminData = {
            id: adminIdInput.value,
            name: adminNameInput.value,
            email: adminEmailInput.value
        };

        if (editingAdminIndex === null) {
            admins.push(adminData);
        } else {
            admins[editingAdminIndex] = adminData;
        }

        renderAdmins();
        closeModal();
    });

    window.editAdmin = (index) => {
        const admin = admins[index];
        adminIdInput.value = admin.id;
        adminNameInput.value = admin.name;
        adminEmailInput.value = admin.email;
        editingAdminIndex = index;
        openModal('Editar Administrativo');
    };

    window.deleteAdmin = (index) => {
        admins.splice(index, 1);
        renderAdmins();
    };

    renderAdmins();
});