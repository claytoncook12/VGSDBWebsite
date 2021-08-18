function searchTuneType() {
    // Declare variables
    var tune, type, tune_filter, type_filter, table, tr, td, i, txtValue;
    tune = document.getElementById("tuneName");
    type = document.getElementById("typeName");
    keys = document.getElementById('keyName');
    tune_filter = tune.value.toUpperCase();
    type_filter = type.value.toUpperCase();
    key_filter = keys.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    // Both tune, type, and key Conditions Present
    if ( tune_filter &&  type_filter && key_filter){
        for (i = 0; i < tr.length; i++) {
        td_tune = tr[i].getElementsByTagName("td")[0];
        td_type = tr[i].getElementsByTagName("td")[1];
        td_key = tr[i].getElementsByTagName("td")[2];
            if (td_tune || td_type || td_key) {
                tune_txtValue = td_tune.textContent || td_tune.innerText;
                type_txtValue = td_type.textContent || td_type.innerText;
                key_txtValue = td_key.textContent || td_key.innerText;
                if (tune_txtValue.toUpperCase().indexOf(tune_filter) > -1 &&
                    type_txtValue.toUpperCase().indexOf(type_filter) > -1 &&
                    key_txtValue.toUpperCase().indexOf(key_filter) > -1) {
                tr[i].style.display = "";
                } else {
                tr[i].style = "display: none!important;";
                }
            }
        }
    }
    
    // Both tune and type Conditions Present
    else if ( tune_filter &&  type_filter){
        for (i = 0; i < tr.length; i++) {
        td_tune = tr[i].getElementsByTagName("td")[0];
        td_type = tr[i].getElementsByTagName("td")[1];
            if (td_tune || td_type) {
                tune_txtValue = td_tune.textContent || td_tune.innerText;
                type_txtValue = td_type.textContent || td_type.innerText;
                if (tune_txtValue.toUpperCase().indexOf(tune_filter) > -1 &&
                    type_txtValue.toUpperCase().indexOf(type_filter) > -1) {
                tr[i].style.display = "";
                } else {
                tr[i].style = "display: none!important;";
                }
            }
        }
    }

    // Both tune and key Conditions Present
    else if ( tune_filter &&  key_filter){
        for (i = 0; i < tr.length; i++) {
        td_tune = tr[i].getElementsByTagName("td")[0];
        td_key = tr[i].getElementsByTagName("td")[2];
            if (td_tune || td_key) {
                tune_txtValue = td_tune.textContent || td_tune.innerText;
                key_txtValue = td_key.textContent || td_key.innerText;
                if (tune_txtValue.toUpperCase().indexOf(tune_filter) > -1 &&
                    key_txtValue.toUpperCase().indexOf(key_filter) > -1) {
                tr[i].style.display = "";
                } else {
                tr[i].style = "display: none!important;";
                }
            }
        }
    }

    // Both type and key Conditions Present
    else if ( type_filter &&  key_filter){
        for (i = 0; i < tr.length; i++) {
        td_type = tr[i].getElementsByTagName("td")[1];
        td_key = tr[i].getElementsByTagName("td")[2];
            if (td_type || td_key) {
                type_txtValue = td_type.textContent || td_type.innerText;
                key_txtValue = td_key.textContent || td_key.innerText;
                if (type_txtValue.toUpperCase().indexOf(type_filter) > -1 &&
                    key_txtValue.toUpperCase().indexOf(key_filter) > -1) {
                tr[i].style.display = "";
                } else {
                tr[i].style = "display: none!important;";
                }
            }
        }
    }

    // If Tune Present Filter
    else if ( tune_filter ) {
        for (i = 0; i < tr.length; i++) {
        td_tune = tr[i].getElementsByTagName("td")[0];
            if (td_tune) {
                tune_txtValue = td_tune.textContent || td_tune.innerText;
                if (tune_txtValue.toUpperCase().indexOf(tune_filter) > -1) {
                tr[i].style.display = "";
                } else {
                tr[i].style = "display: none!important;";
                }
            }
        }
    }

    // If Type Present Filter
    else if ( type_filter ){
        for (i = 0; i < tr.length; i++) {
        td_type = tr[i].getElementsByTagName("td")[1];
            if (td_type) {
                type_txtValue = td_type.textContent || td_type.innerText;
                if (type_txtValue.toUpperCase().indexOf(type_filter) > -1) {
                tr[i].style.display = "";
                } else {
                tr[i].style = "display: none!important;";
                }
            }
        }
    }

    // If Key Present Filter
    else {
        for (i = 0; i < tr.length; i++) {
        td_key = tr[i].getElementsByTagName("td")[2];
            if (td_key) {
                key_txtValue = td_key.textContent || td_key.innerText;
                if (key_txtValue.toUpperCase().indexOf(key_filter) > -1) {
                tr[i].style.display = "";
                } else {
                tr[i].style = "display: none!important;";
                }
            }
        }
    }
  }