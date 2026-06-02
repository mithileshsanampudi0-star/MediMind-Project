document.addEventListener("DOMContentLoaded", () => {

    console.log("Analytics Loaded");

    const scoreElement = document.getElementById("healthScore");

    if(scoreElement){

        let score = parseInt(scoreElement.innerText);

        if(score >= 80){
            scoreElement.style.color = "#00ff88";
        }
        else if(score >= 50){
            scoreElement.style.color = "#ffcc00";
        }
        else{
            scoreElement.style.color = "#ff4d6d";
        }
    }

});