function random(sta, ct) {
    var sta = document.getElementById(sta);
    var ct = document.getElementById(ct);

    ct.innerHTML = "";

    if (sta.value == "bihar") {
        var optionArray = ['patna|Patna', 'hajipur|Hajipur', 'darbhanga|Darbhanga', 'danapur|Danapur', 'sonpur|Sonpur'];
    }
    else if (sta.value == "delhi") {
        var optionArray = ['gazu|Gcbce', 'efwef|Escbcb'];
    }
    for (var option in optionArray) {
        var pair = optionArray[option].split("|");
        var newoption = document.createElement("option");
        newoption.value = pair[0];
        newoption.innerHTML = pair[1];

        ct.options.add(newoption);
    }
}