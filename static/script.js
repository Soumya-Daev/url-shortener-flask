function myFunction() {
    /* Get the text field */
    var copyText = document.getElementById("shortUrl");
  
    /* Select the text field */
    myText = copyText.innerHTML;
  
     /* Copy the text inside the text field */
    navigator.clipboard.writeText(myText);
  
    /* Alert the copied text */
    alert("Copied the text: " + myText);
  }