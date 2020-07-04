declare var L: any;

import store from "./src/store";
import { Question, QuizState, cleanupQuestion} from "./src/models";

async function init(){
    let urlSplit = window.location.href.split("/");
    let slug = urlSplit[urlSplit.length-2];
    let dataRequest = await fetch(`/api/quiz/${slug}`);
    let data = await dataRequest.json();
    let mapData = JSON.parse(data.map.content);

    store.subscribe(updatePage);

    let questions = cleanupQuestion(data.questions as any[]);
    store.setQuestions(questions);

    let info = document.getElementById("info");
    if(info !== null){
        info.textContent = data.description;
    }
    setInterval(()=>{
        store.tick();
    },1000);


    let map = L.map("map",{attributionControl: false}).setView([40.416775, -3.703790], 6);


    function style(features: any){
        return {
            fillColor: "#37c837",
            weight: 1,
            opacity: 1,
            color: "black",
            dashArray: "1",
            fillOpacity: 0.7
        };
    }

    function onEachFeature(feature: any, layer: any){
        layer.on("click",(e: any)=>{
            let props = e.target.feature.properties;
            store.submitAnswer(props.mapaly_id);
        });
    }

    L.geoJSON(mapData,{
        style: style,
        onEachFeature: onEachFeature,
        attribution: data.map.license
    })
    .addTo(map);
}

function updatePage(state: QuizState){
    const score = document.getElementById("points");
    if(score){
        score.textContent = `${state.score}`;
    }
    const time = document.getElementById("time-string");
    if(time){
        const minutes = Math.floor(state.time / 60);
        const seconds = state.time % 60;
        const secondsStr = seconds < 10 ? `0${seconds}` : `${seconds}`;
        time.textContent = `${minutes}:${secondsStr}`;
    }
    const question = document.getElementById("question");
    if(question && state.activeQuestion){
        question.textContent = state.activeQuestion.question;
    }
    if(question && state.activeQuestion === null){
        question.textContent = "VICTORIA";
    }
}

window.addEventListener("load",function(){
    init().then(()=>{
        console.log("OK");
    }).catch((e)=>{
        console.log("ERROR");
        console.error(e);
    });
});



