// vim: set expandtab shiftwidth=4 softtabstop=4:

columns = [{}, {}]

function make_button(btype, name, value, text, checked) {
    var label = document.createElement("label");
    var btn = document.createElement("input");
    btn.type = btype;
    btn.name = name;
    btn.value = value;
    btn.checked = checked;
    btn.onclick = update_plot;
    label.appendChild(btn);
    label.appendChild(document.createTextNode(text));
    return label;
}

function reload() {
    var table = document.getElementById("column_table");
    // Save sort and shown columns
    var sort_column = null;
    var sort_buttons = document.getElementsByName("sort")
    for (var i = 0; i < sort_buttons.length; i++)
        sort_column = sort_buttons[i].value;
    var show_columns = [];
    var show_buttons = document.getElementsByName("show")
    for (var i = 0; i < show_buttons.length; i++) {
        var e = show_buttons[i];
        if (e.checked && columns[0].includes(e.value))
            show_columns.push(e.value);
    }
    if (show_columns.length == 0)
        show_columns.push(Object.keys(columns[0])[0])
    // Clear out the table and fill in with text
    // then numeric column names
    while (table.hasChildNodes())
        table.removeChild(table.lastChild);
    for (r in columns[1]) {
        var tr = document.createElement("tr");
        table.appendChild(tr);
        var td0 = document.createElement("td");
        tr.appendChild(td0);
        var td1 = document.createElement("td");
        td1.textContent = r;
        tr.appendChild(td1);
        var td2 = document.createElement("td");
        tr.appendChild(td2);
    }
    for (r in columns[0]) {
        var tr = document.createElement("tr");
        table.appendChild(tr);
        var td0 = document.createElement("td");
        td0.appendChild(make_button("radio", "sort", r, "sort",
                                    r == sort_column));
        td0.appendChild(make_button("checkbox", "show", r, "show",
                                    show_columns.includes(r)));
        tr.appendChild(td0);
        var td1 = document.createElement("td");
        td1.textContent = r;
        tr.appendChild(td1);
        var td2 = document.createElement("td");
        tr.appendChild(td2);
    }
    update_plot();
}

function update_plot() {
    var opts = { xaxes: [ { }, { show: false } ] }
    var ids = columns[1]["Id"]
    var order = ids.map(function(e, i) { return i; });
    var series = [];
    var numeric = columns[0];
    var show_buttons = document.getElementsByName("show")
    for (var i = 0; i < show_buttons.length; i++) {
        var e = show_buttons[i];
        if (!e.checked)
            continue;
        var label = e.value;
        var data = numeric[label];
        series.push({ label: label,
                      points: { show: true },
                      xaxis: 2,
                      data: order.map(function(e, i) { return [e, data[i]]; })
                    })
    }
    $.plot("#data", series, opts);
}

function init() {
    $(document).ready(function() {
        // initialization
        ;
    });
}
