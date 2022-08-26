// Add Tune Set Start and End Time Button Functions

// Take Youtube Video Obj and Return HH:MM:SS Text
// Will Only work if time is less than 24 hours
const youtubePlayerToTimestamp = (youtubePlayer) => {
    var date = new Date(null);
    date.setSeconds(youtubePlayer.getCurrentTime()); // specify video current time in seconds
    var result = date.toISOString().substring(11,11+8);
    return result  
}

// Get Buttons and Setup Click Events
const btnStartTime = document.getElementById("start-time");
const btnEndTime = document.getElementById("end-time");

const btnAddStartTime = document.getElementById('startTimeYoutubeVideoAddBtn');
const btnAddEndTime = document.getElementById('endTimeYoutubeVideoAddBtn');

btnAddStartTime.addEventListener('click', () => {
    btnStartTime.value = youtubePlayerToTimestamp(player);
});
btnAddEndTime.addEventListener('click', () => {
    btnEndTime.value = youtubePlayerToTimestamp(player);
});