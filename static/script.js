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