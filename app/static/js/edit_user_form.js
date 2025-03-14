//<script>
//document.addEventListener('DOMContentLoaded', function() {
//    var editUserModal = document.getElementById('editUserModal');
//    editUserModal.addEventListener('show.bs.modal', function (event) {
//        var button = event.relatedTarget; // Кнопка, которая вызвала модальное окно
//        var userId = button.getAttribute('data-user-id');
//        var username = button.getAttribute('data-username');
//        var email = button.getAttribute('data-email');
//        var role = button.getAttribute('data-role');
//
//        // Заполняем форму редактирования
//        document.getElementById('editUsername').value = username;
//        document.getElementById('editEmail').value = email;
//        document.getElementById('editRole').value = role;
//
//        // Устанавливаем action формы
//        document.getElementById('editUserForm').action = "/admin/edit_user/" + userId;
//    });
//});
//</script>