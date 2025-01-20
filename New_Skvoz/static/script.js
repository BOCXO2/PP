$(document).ready(function() {
    // Скрываем загрузчик после того, как страница полностью загружена
    $(window).on('load', function() {
        $('#loader').fadeOut(500);  // Плавно скрываем загрузчик за 500 мс
        $('body').css('overflow', 'auto'); // Разрешаем прокрутку
    });

    // В случае, если загрузка затянулась, используем таймер, чтобы скрыть загрузчик через 3 секунды
    setTimeout(function() {
        $('#loader').fadeOut(500);
        $('body').css('overflow', 'auto');
    }, 3000);

    $("#uploadForm").submit(function(event) {
        event.preventDefault();

        var formData = new FormData(this);
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            success: function(response) {
                if (response.message) {
                    $("#result").html(`
                        <p class="text-success">${response.message}</p>
                        <a href="${response.output_file}" class="btn btn-success" download>Download Processed File</a>
                    `);
                } else {
                    $("#result").html('<p class="text-danger">Error: ' + response.error + '</p>');
                }
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
});
