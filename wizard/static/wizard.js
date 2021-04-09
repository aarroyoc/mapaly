class DataService {
    constructor(dataUrl){
        this.dataUrl = dataUrl;
    }

    async getIndex() {
        const response = await fetch(`${this.dataUrl}index.json`);
        const json = await response.json();
        return json;
    }

}

class Round {
    constructor(win, others) {
        this.win = win;
        this.others = others;
    }

    static random(n) {
        return Math.floor(Math.random() * n);
    }

    static randomRoundFromCityIds(set) {
        const ids = Array.from(set);
        const winIndex = this.random(ids.length);
        const win = ids[winIndex];
        ids.splice(winIndex, 1);
        const others = [];
        for(let i=0;i<3;i++){
            const otherIndex = this.random(ids.length);
            const other = ids[otherIndex];
            ids.splice(otherIndex, 1);
            others.push(other);
        }
        return new Round(win, others);
    }
}

class Game {
    constructor(dataUrl, grid, index) {
        this.scoreText = document.getElementById("score");
        this.bar = document.getElementById("bar");
        this.dataUrl = dataUrl;
        this.score = 0;
        this.grid = grid;
        this.index = index;
        this.cityIds = new Set(index.cities.map((city) => city.id));
        this.round = null;
    }

    showSatellite() {
        const img = new Image();
        img.src = `${this.dataUrl}${this.round.win}.jpg`;
        img.className = "bigImg";
        this.grid.appendChild(img);
        img.onload = () => {
            const timeBar = document.createElement("div");
            timeBar.className = "timeBar";
            this.bar.appendChild(timeBar);
            setTimeout(() => {
                img.remove();
                timeBar.remove();
                this.showMaps();
            }, 2000);

        }
    }

    showGameOver() {
        document.getElementById("game-over").style.display = "initial";
        document.getElementById("game-over-text").style.display = "initial";
    }

    showMaps() {
        const win = new Image();
        win.src = `${this.dataUrl}${this.round.win}.png`;
        const other1 = new Image();
        other1.src = `${this.dataUrl}${this.round.others[0]}.png`;
        const other2 = new Image();
        other2.src = `${this.dataUrl}${this.round.others[1]}.png`;
        const other3 = new Image();
        other3.src = `${this.dataUrl}${this.round.others[2]}.png`;
        const images = shuffleArray([win, other1, other2, other3]);
        images.forEach(img => img.className = "smallImg");
        this.grid.className = "smallQuadra";
        this.grid.appendChild(images[0]);
        this.grid.appendChild(images[1]);
        this.grid.appendChild(images[2]);
        this.grid.appendChild(images[3]);
        win.onclick = () => {
            this.score += 1;
            images.map(img => img.remove());
            this.startRound();
        };
        other1.onclick = () => {
            images.map(img => img.remove());
            this.showGameOver();
        };
        other2.onclick = () => {
            images.map(img => img.remove());
            this.showGameOver();
        };
        other3.onclick = () => {
            images.map(img => img.remove());
            this.showGameOver();
        };
    }

    startRound() {
        this.scoreText.textContent = `Score: ${this.score}`;
        this.grid.className = "";
        this.round = Round.randomRoundFromCityIds(this.cityIds);
        this.showSatellite();
    }
}

const shuffleArray = (originArray) => {
    const array = originArray.slice();
    const shuffled = new Array;
    while(array.length > 0){
        const n = Math.floor(Math.random() * array.length);
        shuffled.push(array.splice(n, 1)[0]);
    }
    return shuffled;
};

function main() {
    const wizardDataUrl = document.getElementById("wizard-data-url").value;
    const quadra = document.getElementById("quadra");
    const dataService = new DataService(wizardDataUrl);
    dataService.getIndex().then(index => {
        const game = new Game(wizardDataUrl, quadra, index);
        const playButton = document.getElementById("play");
        playButton.addEventListener("click", () => {
            playButton.remove();
            game.startRound();
        });
    });
    document.getElementById("reload").onclick = () => window.location.reload();
    
}
main();