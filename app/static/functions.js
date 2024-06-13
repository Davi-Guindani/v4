function updateCheckboxes() {
    const classSelect = document.getElementById('class');
    const listDiv = document.getElementById('list');
    const selectedClass = classSelect.value;

    const options = {
        segqua0708: [
            { value: 'manel', text: 'Manel' },
            { value: 'bernardo', text: 'Bernardo' },
            { value: 'pipico', text: 'Pipico' }
        ],
        segqua1112: [
            { value: 'ana', text: 'Ana' },
            { value: 'alice', text: 'Alice' },
            { value: 'andré', text: 'André' },
        ],
        segqua2122: [
            { value: 'thales', text: 'Thales' },
            { value: 'amanda', text: 'Amanda' },
            { value: 'letícia', text: 'Letícia' },
        ],
        terqui0910: [
            { value: 'natasha', text: 'Natasha' },
            { value: 'luiza', text: 'Luiza' },
            { value: 'gabriela', text: 'Gabriela' },
        ],
        terqui1314: [
            { value: 'mariana', text: 'Mariana' },
            { value: 'davi', text: 'Davi' },
            { value: 'eduardo', text: 'Eduardo' },
        ],
        terqui1415: [
            { value: 'rafael', text: 'Rafael' },
            { value: 'jennifer', text: 'Jennifer' },
            { value: 'luiz', text: 'Luiz' },
        ]
    };

    // Limpar opções atuais
    listDiv.innerHTML = '';

     // Adicionar novas checkboxes com base na seleção
     if (selectedClass) {
        options[selectedClass].forEach(option => {
            const checkboxContainer = document.createElement('div');
            checkboxContainer.className = 'checkbox-container';

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = option.value;
            checkbox.name = 'specific[]';
            checkbox.value = option.value;

            const label = document.createElement('label');
            label.htmlFor = option.value;
            label.textContent = option.text;

            checkboxContainer.appendChild(checkbox);
            checkboxContainer.appendChild(label);
            listDiv.appendChild(checkboxContainer);
        });
    }
}

function gatherCheckboxValues() {
    const checkboxes = document.querySelectorAll('.checkbox-container input[type="checkbox"]:checked');
    const values = Array.from(checkboxes).map(checkbox => checkbox.nextElementSibling.textContent.trim());
    return values.join(', ');
}

document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    const listInput = document.createElement('input');
    listInput.type = 'hidden';
    listInput.name = 'list';
    listInput.value = gatherCheckboxValues();
    this.appendChild(listInput);
    this.submit();
});

