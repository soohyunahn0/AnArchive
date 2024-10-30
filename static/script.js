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


function search() {
    let input = document.getElementById('searchbar').value
    input = input.toLowerCase();
    let x = document.getElementsByClassName('animals');
  
    for (i = 0; i < x.length; i++) {
      if (!x[i].innerHTML.toLowerCase().includes(input)) {
        x[i].style.display = "none";
      }
      else {
        x[i].style.display = "list-item";
      }
    }
  }
