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
                    
                    studentsContainer.append(
                        '<input type="checkbox" name="students" value="' + student.id + '"> ' +
                        studentName + '<br>'
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
