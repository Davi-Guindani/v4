$(document).ready(function() {
    $('#class').change(function() {
        var classId = $(this).val(); // Obtém o ID da turma selecionada
        $.ajax({
            url: '/get_students', // URL da rota Flask que vai retornar os alunos
            type: 'GET',
            data: { class_id: classId }, // Dados enviados ao servidor
            success: function(response) {
                var studentsContainer = $('#students-container');
                studentsContainer.empty(); // Limpa o contêiner antes de adicionar novos checkboxes
                response.students.forEach(function(student) {
                    // Capitaliza todas as palavras do nome do aluno
                    var studentName = capitalize(student.name);
                    var studentLastName = capitalize(student.last_name);
                    
                    studentsContainer.append(
                        '<input type="checkbox" name="students" value="' + student.id + '"> ' +
                        studentName + ' ' + studentLastName + '<br>'
                    );
                });
            },
            error: function(error) {
                console.log("Erro ao buscar alunos: ", error);
            }
        });
    });
});

// Função para capitalizar todas as palavras
function capitalize(str) {
    return str.split(' ').map(function(word) {
        return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
    }).join(' ');
}

$(document).ready(function() {
    $('#attendance-form').submit(function(event) {
        event.preventDefault(); // Prevent the form from submitting normally

        const formData = $(this).serialize();

        $.post('/submit', formData, function(response) {
            if (response.error) {
                if (response.error === 'Registro duplicado') {
                    const edit = confirm('Registro duplicado encontrado. Deseja editar o registro existente?');
                    if (edit) {
                        window.location.href = `/edit_attendance/${response.attendance_id}`;
                    }
                } else {
                    alert(response.error);
                }
            } else {
                alert(response.success);
                window.location.reload();
            }
        }).fail(function(jqXHR) {
            const response = jqXHR.responseJSON;
            if (response.error === 'Registro duplicado') {
                const edit = confirm(`Registro duplicado encontrado (ID: ${response.attendance_id}). Deseja editar o registro existente?`);
                if (edit) {
                    window.location.href = `/edit_attendance/${response.attendance_id}`;
                }
            } else {
                alert(response.error);
            }
        });
    });
});

$(document).ready(function() {
    // Verifica se o parâmetro success está presente na URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('success')) {
        alert('Dados atualizados com sucesso!');
        // Remove o parâmetro de query string para evitar múltiplos alertas
        urlParams.delete('success');
        window.history.replaceState({}, document.title, window.location.pathname);
    }

});