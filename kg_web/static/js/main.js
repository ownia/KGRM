$(function () {
    //禁用"确认重新提交表单"
    window.history.replaceState(null, null, window.location.href);
});

// document.getElementById("slogan").style.height = document.getElementById("img").offsetHeight + "px";

// document.forms[0].target="iframeForm";

/*
document.getElementById("cypher").value = localStorage.getItem("comment");

function saveComment() {
    var comment = document.getElementById("cypher").value;
    if (comment == "") {
        alert("Please enter a comment in first!");
        return false;
    }

    localStorage.setItem("comment", comment);
    alert("Your comment has been saved!");

    location.reload();
    return false;
    //return true;
}*/
