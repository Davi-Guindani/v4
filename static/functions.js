function updateCheckboxes() {
    const classSelect = document.getElementById('class');
    const listDiv = document.getElementById('list');
    const selectedClass = classSelect.value;

    const options = {
        segqua0708: [
            { value: 'Manel', text: 'Manel' },
            { value: 'Bernardo', text: 'Bernardo' },
            { value: 'Pipico', text: 'Pipico' }
        ],
        segqua1112: [
            { value: 'Ana', text: 'Ana' },
            { value: 'Alice', text: 'Alice' },
            { value: 'André', text: 'André' },
        ],
        segqua2122: [
            { value: 'Thales', text: 'Thales' },
            { value: 'Amanda', text: 'Amanda' },
            { value: 'Letícia', text: 'Letícia' },
        ],
        terqui0910: [
            { value: 'Natasha', text: 'Natasha' },
            { value: 'Luiza', text: 'Luiza' },
            { value: 'Gabriela', text: 'Gabriela' },
        ],
        terqui1314: [
            { value: 'Mariana', text: 'Mariana' },
            { value: 'Davi', text: 'Davi' },
            { value: 'Eduardo', text: 'Eduardo' },
        ],
        terqui1415: [
            { value: 'Rafael', text: 'Rafael' },
            { value: 'Jennifer', text: 'Jennifer' },
            { value: 'Luiz', text: 'Luiz' },
        ]
    };

    // Limpar opções atuais
    listDiv.innerHTML = '';

    // // Adicionar novas checkboxes com base na seleção
    // options[selectedClass].forEach(option => {
    //     const checkbox = document.createElement('input');
    //     checkbox.type = 'checkbox';
    //     checkbox.id = option.value;
    //     checkbox.name = 'specific[]';   
    //     checkbox.value = option.value;

    //     const label = document.createElement('label');
    //     label.htmlFor = option.value;
    //     label.textContent = option.text;

    //     listDiv.appendChild(checkbox);
    //     listDiv.appendChild(label);
    //     listDiv.appendChild(document.createElement('br'));
    // });

     // Adicionar novas checkboxes com base na seleção
     if (selectedClass && options[selectedClass]) {
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
    const values = Array.from(checkboxes).map(checkbox => {
        const label = document.querySelector(`label[for="${checkbox.id}"]`);
        return label ? label.textContent.trim() : checkbox.value;
    }); 
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

