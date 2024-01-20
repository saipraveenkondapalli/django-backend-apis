window.onload = function() {
    console.log("start onload");
    var select = document.getElementById("id_country");
    var searchBox = document.createElement("input");
    searchBox.type = "text";
    searchBox.id = "searchBox";
    searchBox.onkeyup = function() {
        var filter = searchBox.value.toUpperCase();
        var options = select.options;
        for (var i = 0; i < options.length; i++) {
            var txtValue = options[i].text;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                options[i].style.display = "";
            } else {
                options[i].style.display = "none";
            }
        }
    };
    select.insertBefore(searchBox, select.firstChild);
};