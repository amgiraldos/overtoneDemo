const stages = ["RED", "YELLOW", "GREEN", "DECISION"];
const durations = {
    RED: 5000,
    YELLOW: 7000,
    GREEN: 5000,
    DECISION: 6000
};

const labels = {
    EN: {
        RED: "STOP",
        YELLOW: "BREATHE",
        GREEN: "THINK",
        DECISION: "NOW YOU CAN DECIDE"
    },
    ES: {
        RED: "ALTO",
        YELLOW: "RESPIRA",
        GREEN: "PIENSA",
        DECISION: "AHORA PUEDES DECIDIR"
    }
};

let currentStageIndex = 0;
let currentLanguage = "EN";

const red = document.getElementById("red");
const yellow = document.getElementById("yellow");
const green = document.getElementById("green");
const labelEl = document.getElementById("label");
const langBtn = document.getElementById("languageToggle");
const soundBtn = document.getElementById("soundToggle");
const audio = document.getElementById("bgAudio");

langBtn.addEventListener("click", () => {
    currentLanguage = currentLanguage === "EN" ? "ES" : "EN";
    langBtn.textContent = currentLanguage === "EN" ? "ES" : "EN";
});

soundBtn.addEventListener("click", () => {
    if (audio.paused) {
        audio.play();
        soundBtn.textContent = "🔊";
    } else {
        audio.pause();
        soundBtn.textContent = "🔈";
    }
});

function updateStage() {
    const stage = stages[currentStageIndex];
    const duration = durations[stage] / 1000;
    let timeLeft = duration;

    // Reset
    red.style.backgroundColor = "#333";
    yellow.style.backgroundColor = "#333";
    green.style.backgroundColor = "#333";
    red.style.boxShadow = yellow.style.boxShadow = green.style.boxShadow = "none";

    // Color y luz activa
    switch (stage) {
        case "RED":
            red.style.backgroundColor = "#EF4444";
            red.style.boxShadow = "0 0 15px #f87171";
            break;
        case "YELLOW":
            yellow.style.backgroundColor = "#FACC15";
            yellow.style.boxShadow = "0 0 15px #fde68a";
            break;
        case "GREEN":
            green.style.backgroundColor = "#4ADE80";
            green.style.boxShadow = "0 0 15px #6ee7b7";
            break;
        case "DECISION":
            const white = "#f0f0f0";
            red.style.backgroundColor = white;
            yellow.style.backgroundColor = white;
            green.style.backgroundColor = white;
            red.style.boxShadow = yellow.style.boxShadow = green.style.boxShadow = "0 0 10px white";
            break;
    }

    labelEl.textContent = labels[currentLanguage][stage];
    const countdownEl = document.getElementById("countdown");

    if (stage !== "DECISION") {
        countdownEl.textContent = timeLeft;

        const countdownInterval = setInterval(() => {
            timeLeft--;
            countdownEl.textContent = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(countdownInterval);
            }
        }, 1000);
    } else {
        countdownEl.textContent = ""; // No mostrar contador en etapa final
    }

    setTimeout(() => {
        currentStageIndex = (currentStageIndex + 1) % stages.length;
        updateStage();
    }, durations[stage]);
}


updateStage();
