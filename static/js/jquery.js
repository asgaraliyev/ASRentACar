

function filterSelection(c) {
    if (c == "all") {
        $("#cars-lits .sport").fadeIn();
        $("#cars-lits .business").fadeIn();
        $("#cars-lits .full-size").fadeIn();
        $("#cars-lits .minivan").fadeIn();
        $("#cars-lits .economy").fadeIn();
    } else {
        $("#cars-lits .sport").fadeOut();
        $("#cars-lits .business").fadeOut();
        $("#cars-lits .full-size").fadeOut();
        $("#cars-lits .minivan").fadeOut();
        $("#cars-lits .economy").fadeOut();
        $("#cars-lits ." + c).fadeIn();
    }
}
function gotolink(selectValue){
    Cookies.set("currency",selectValue)
    window.location.href="/changemoney/"+selectValue
}
function changecurrency(){
        var selectValue = $('#money .currency').val();
        gotolink(selectValue)
       
}
$('#money .currency').on('change', function(){
    var selectValue = $(this).val();
    gotolink(selectValue)
});

$('.lang').on('change', function(){
    var selectValue = $(this).val();
    Cookies.set("language",selectValue)
    window.location.href="/"
});
function changelanguage(){
    var selectValue = $('#language .lang').val();
    Cookies.set("language",selectValue)
    window.location.href="/"
}