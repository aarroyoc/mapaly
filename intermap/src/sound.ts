declare var L: any;

export class Sound{
    private okSfx: HTMLAudioElement;
    private badSfx: HTMLAudioElement;

    constructor(){
        this.okSfx = new Audio("/static/ok.wav");
        this.badSfx = new Audio("/static/bad.wav");
    }

    get muted(){
        return localStorage.getItem("mute") === "muted";
    }

    toggle(){
        if(this.muted){
            localStorage.setItem("mute", "");
        }else{
            localStorage.setItem("mute", "muted");
        }
    }

    playOk(){
        if(!this.muted){
            this.okSfx.currentTime = 0;
            this.okSfx.play();
        }
    }

    playBad(){
        if(!this.muted){
            this.badSfx.currentTime = 0;
            this.badSfx.play();
        }
    }
}

export function SoundControl(sound: Sound){
    const control = L.control();
    const update = (img: HTMLImageElement) => {
        if(sound.muted){
            img.src = "/static/volume-off.svg";
        }else{
            img.src = "/static/volume-on.svg";
        }
    }
    control.onAdd = (map: any) => {
        const img = new Image();
        img.className = "volume";
        update(img);
        img.onclick = () => {
            sound.toggle();
            update(img);
        };
        return img;
    };
    return control;
}