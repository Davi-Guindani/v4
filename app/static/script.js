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
                    studentsContainer.append(
                        '<input type="checkbox" name="students" value="' + student.id + '"> ' +
                        student.name + '<br>'
                    );
                });
            },
            error: function(error) {
                console.log("Erro ao buscar alunos: ", error);
            }
        });
    });
});
