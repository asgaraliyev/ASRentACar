$('#nmberone').click(function () {
    $('#mainCoantiner, #formBg').removeClass('mystyleSec');
    $('#mainCoantiner, #formBg').removeClass('mystylethird');
    event.stopPropagation();
});



$('#nmbertwo').click(function () {
    $('#mainCoantiner, #formBg').removeClass('mystylethird');
    $('#mainCoantiner, #formBg').addClass('mystyleSec');
    event.stopPropagation();
});


$('#numberthree').click(function () {
    /* $('#catbox').removeClass('cat2');*/
    $('#mainCoantiner, #formBg').addClass('mystylethird');
    event.stopPropagation();
});