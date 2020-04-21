import * as L from "../leaflet-1.6/leaflet-src.esm.js";

class Quest {
    constructor(){
        this.questions = JSON.parse(document.getElementById("quiz-data").textContent).questions;
        this.currentQuestion = -1;
    }

    checkAnswer(id){
        return id === this.questions[this.currentQuestion].answer;
    }

    nextQuestion(){
        this.currentQuestion++;
        if(!this.finished){
            return this.questions[this.currentQuestion].question;
        }else{
            return null;
        }
    }

    get finished(){
        return this.currentQuestion === this.questions.length;
    }

}

function main(){
    let map = L.map("map",{attributionControl: false}).setView([40.416775, -3.703790], 6);
    let quest = new Quest();
    /*L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);*/

    let mapDataDOM = document.getElementById("geojson-map");
    let mapData = JSON.parse(mapDataDOM.textContent);

    function style(features){
        return {
            fillColor: "#800026",
            weight: 2,
            opacity: 1,
            color: "black",
            dashArray: "3",
            fillOpacity: 0.7
        };
    }

    function onEachFeature(feature, layer){
        layer.on("click",check);
    }

    function check(e){
        let props = e.target.feature.properties;
        if(!quest.finished){
            if(quest.checkAnswer(props.mapaly_id)){
                // SONIDO VICTORIA
                let question = quest.nextQuestion();
                if(question !== null){
                    info.update(question);
                }else{
                    info.update("VICTORIA");
                }
            }else{
                // ERROR
            }
        }
    }

    L.geoJSON(mapData, {
        style: style,
        onEachFeature: onEachFeature,
        attribution: "Creative Commons 4.0 BY"
    }).addTo(map);


    let info = L.control();
    info.onAdd = function(){
        this._div = L.DomUtil.create("div", "info");
        this.update();
        return this._div;
    };
    info.update = function(question){
        this._div.innerHTML = `<h5>¿Dónde está?</h5><br><h4>${question}</h4>`;
    };
    info.addTo(map);

    info.update(quest.nextQuestion());

}

window.addEventListener("load", main);