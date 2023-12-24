function hire() {
    var firstname_textbox = document.getElementById("firstname");
    var middlename_textbox = document.getElementById("middlename");
    var lastname_textbox = document.getElementById("lastname");
    var jobtitle_textbox = document.getElementById("jobtitle");
    var firstname = firstname_textbox.value;
    var middlename = middlename_textbox.value;
    var lastname = lastname_textbox.value;
    var jobtitle = jobtitle_textbox.value;
    jobtitle = jobtitle.replaceAll(" ", "_");
    
    window.location.href='/hire/' + '/' + firstname + '/' + middlename + '/' + lastname + '/' + jobtitle;
}
