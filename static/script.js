n =  new Date();
y = n.getFullYear();
m = n.getMonth() + 1;
d = n.getDate();
hour = n.getHours();
minute = n.getMinutes();
if(minute < 10){
    minute = "0" + minute;
}

if(hour > 12){
    hour = hour - 12;
}

if(hour < 10){
    hour = "0" + hour;
}
document.getElementById("date").innerHTML = hour + ":" + minute + " | " + m + "/" + d + "/" + y;

function submitForm() {
    document.getElementById('myForm').submit();
}

$(document).ready(function() {
      $('#scrapeForm').on('submit', function(e) {
        // Get references to the button elements
        const scrapeBtn = $('#scrapeBtn');
        const btnText = $('#btnText');
        const loadingSpinner = $('#loadingSpinner');
        
        // Show loading state
        btnText.text('Loading...');
        loadingSpinner.show();
        scrapeBtn.prop('disabled', true);
        
        // Optional: Add a timeout to reset the button if something goes wrong
        setTimeout(function() {
          // Only reset if the page hasn't redirected/reloaded
          if (scrapeBtn.prop('disabled')) {
            btnText.text('Scrape Link');
            loadingSpinner.hide();
            scrapeBtn.prop('disabled', false);
          }
        }, 30000); // 30 second timeout
      });
});