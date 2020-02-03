function add_setting(){
        var opt1 = document.getElementById("sel1");
        var evnt = opt1.options[opt1.selectedIndex].value;

        var opt2 = document.getElementById("sel2");
        var actn = opt2.options[opt2.selectedIndex].value;

		var cmd = document.getElementById("command_num").value;
    var fwd_ip = document.getElementById("forward_ip").value;
		console.log(cmd);
		
        var i;
        var txt;
        var ctype = document.ctype;
        for (i = 0; i < ctype.length; i++) {
          if (ctype[i].checked) {
            txt = ctype[i].value;
          }
        }

        if (txt == "device"){
          var js_file = {
          "commandID": cmd,
          "commandDetails": {
              "deviceID": "RPI",
              "signal": evnt,
              "commType": txt,
              "sayThis":actn
            }
          }
        }

        else{
          var js_file = {
            "commandID": cmd,
            "commandDetails": {
              "deviceID": "RPI",
              "targetIP": "http://" + fwd_ip + "/report",
              "signal": evnt,
              "commType": "forward"
            }
          }
        }
        
        console.log(txt)
        console.log(js_file)

        xmlhttp = new XMLHttpRequest();
        var url = document.location +"config";
        console.log(url);
        xmlhttp.open("POST", url, true);
        console.log(js_file,null)
        xmlhttp.setRequestHeader("Content-type", "application/json");
        xmlhttp.send(JSON.stringify(js_file,null));
}

function createTable(tableData) {
  var tableBody = document.createElement('tbody');

  //TABLE HEADERS
  var row = document.createElement('tr');
  var cell = document.createElement('td');
  cell.appendChild(document.createTextNode("Event"));
  row.appendChild(cell);
  var cell = document.createElement('td');
  cell.appendChild(document.createTextNode("Action"));
  row.appendChild(cell);
  tableBody.appendChild(row);

  tableData.forEach(function(rowData) {
    var row = document.createElement('tr');

    rowData.forEach(function(cellData) {
      var cell = document.createElement('td');
      cell.appendChild(document.createTextNode(cellData));
      row.appendChild(cell);
    });

    tableBody.appendChild(row);
  });

  document.getElementById("tbl").innerHTML = "";
  document.getElementById("tbl").appendChild(tableBody);
}
