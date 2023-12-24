var selectedRows = [];
        window.onload = function() {
            var rows = document.getElementsByTagName("tr");
            for (var i = 0; i < rows.length; i++) {
                rows[i].addEventListener("click", function() {
                    var index = selectedRows.indexOf(this);
                    if (this.style.backgroundColor === "lightblue") {
                        this.style.backgroundColor = "";
                        selectedRows.splice(index, 1);
                    } else {
                        this.style.backgroundColor = "lightblue";
                        selectedRows.push(this);
                    }
                });
            }
        };

        function hire() {
        if (selectedRows.length == 1){
            alert("This person is already hired.");
        }
        else if(selectedRows.length > 1){
            alert("These people are already hired.");
        } 
        else {
            window.location.href='/hire';
        }
    };

        function fire() {
            if(selectedRows.length > 1){
                alert("You can only fire one person at a time.");
            }
            else if (selectedRows) {
                var lastTd = selectedRows[0].lastElementChild;
                var id = lastTd.innerText;
                window.location.href='/fire/' + id;
            } else {
                alert("Please select a person to fire.");
            }
    };

        function update() {
        if(selectedRows.length > 1){
            alert("You can only update one person at a time.");
        }
        else if (selectedRows) {
            var lastTd = selectedRows[0].lastElementChild;
            var id = lastTd.innerText;
            window.location.href='/update/' + id;
        } else {
            alert("Please select a person to update.");
        }
    };