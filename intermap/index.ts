declare var L: any;

import store from "./src/store";
import style from "./src/style";
import { Sound, SoundControl} from "./src/sound";
import { showDialog, quitDialog } from "./src/dialog";
import { QuizState, cleanupQuestion} from "./src/models";

async function initGame(){
    const sound = new Sound();

    let urlSplit = window.location.href.split("/");
    let slug = urlSplit[urlSplit.length-2];
    let dataRequest = await fetch(`/api/quiz/${slug}`);
    let data = await dataRequest.json();
    let mapData = JSON.parse(data.map.content);

    let clock = setInterval(()=>{
        store.tick();
    },1000);

    store.subscribe(updatePage(clock));

    let questions = cleanupQuestion(data.questions as any[]);
    store.setQuestions(questions);

    let info = document.getElementById("info");
    if(info !== null){
        info.textContent = data.description;
    }

    const map = L.map("map",{attributionControl: false});

    function onEachFeature(feature: any, layer: any){
        layer.on("click",(e: any)=>{
            let props = e.target.feature.properties;
            const result = store.submitAnswer(props.mapaly_id);
            if(result === "ok"){
                sound.playOk();
                layer.setStyle({fillColor: "#00c800"});
                setTimeout(()=>{
                    layer.setStyle({fillColor: "#14c814"});
                },100);
                setTimeout(()=>{
                    layer.setStyle({fillColor: "#28c828"});
                },200);
                setTimeout(()=>{
                    layer.setStyle({fillColor: "#31c831"});
                },300);
                setTimeout(()=>{
                    layer.setStyle({fillColor: "#37c837"});
                },400);
            }
            if(result === "wrong"){
                sound.playBad();
                layer.setStyle({fillColor: "#c84737"});
                setTimeout(()=>{
                    layer.setStyle({fillColor: "#c85c4f"});
                },100);
                setTimeout(()=>{
                    layer.setStyle({fillColor: "#c87267"});
                },200);
                setTimeout(()=>{
                    layer.setStyle({fillColor: "#c8877f"});
                },300);
                setTimeout(()=>{
                    layer.setStyle({fillColor: "#7fc87f"});
                },400);
                setTimeout(()=>{
                    layer.setStyle({fillColor: "#37c837"});
                },500);
            }

        });
    }

    const geojson = L.geoJSON(mapData,{
        style: style,
        onEachFeature: onEachFeature,
        attribution: data.map.license
    });
    const bounds = geojson.getBounds();
    geojson.addTo(map);
    map.fitBounds(bounds);

    SoundControl(sound).addTo(map);

    document.getElementById("share")?.addEventListener("click", () => showDialog("share-dialog"));
    document.getElementById("close-share-dialog")?.addEventListener("click", () => quitDialog());
    document.getElementById("close-win-dialog")?.addEventListener("click", () => quitDialog());

    document.getElementById("dialog-background")?.addEventListener("click", () => quitDialog());
}

function updatePage(clock: NodeJS.Timeout){
    return (state: QuizState) => {
        const score = document.getElementById("points");
        const scoreDialog = document.getElementById("points-dialog");
        if(score && scoreDialog){
            score.textContent = `${state.score}`;
            scoreDialog.textContent = `${state.score}`;
        }
        const time = document.getElementById("time-string");
        const timeDialog = document.getElementById("time-string-dialog");
        if(time && timeDialog){
            const minutes = Math.floor(state.time / 60);
            const seconds = state.time % 60;
            const secondsStr = seconds < 10 ? `0${seconds}` : `${seconds}`;
            time.textContent = `${minutes}:${secondsStr}`;
            timeDialog.textContent = `${minutes}:${secondsStr}`;
        }
        const question = document.getElementById("question");
        if(question && state.activeQuestion){
            question.textContent = state.activeQuestion.question;
        }
        if(question && state.activeQuestion === null){
            question.textContent = "¡Fin del quiz!";
            clearInterval(clock);
            showDialog("win-dialog");
        }
    }
}

async function initEditor(){
    let urlSplit = window.location.href.split("/");
    let slug = urlSplit[urlSplit.length-2];
    let dataRequest = await fetch(`/api/quiz/${slug}`);
    let data = await dataRequest.json();
    let mapData = JSON.parse(data.map.content);

    let id_answer = document.getElementById("id_answer") as HTMLOutputElement;
    let answer = document.getElementById("answer") as HTMLInputElement;

    let map = L.map("editor-map",{attributionControl: false}).setView([40.416775, -3.703790], 6);

    function onEachFeature(feature: any, layer: any){
        layer.on("click",(e: any)=>{
            let props = e.target.feature.properties;
            id_answer.textContent = props.mapaly_name;
            answer.value = props.mapaly_id;
        });
    }

    L.geoJSON(mapData,{
        style: style,
        onEachFeature: onEachFeature,
        attribution: data.map.license
    })
    .addTo(map);
}

window.addEventListener("load",function(){
    if(document.getElementById("map")){
        initGame().then(()=>{
            console.log("OK");
        }).catch((e)=>{
            console.log("ERROR");
            console.error(e);
        });
    }else{
        initEditor().then(()=>{
            console.log("OK");
        }).catch((e)=>{
            console.log("ERROR");
            console.error(e);
        });
    }
});
