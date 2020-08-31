export function showDialog(id: string){
    let dialog = document.getElementById(id) as HTMLDivElement;
    let dialogBackground = document.getElementById("dialog-background") as HTMLDivElement;
    dialog.style.display = "initial";
    dialogBackground.style.display = "initial";
}

export function quitDialog(){
    let dialogs = document.getElementsByClassName("dialog") as HTMLCollectionOf<HTMLDivElement>;
    let dialogBackground = document.getElementById("dialog-background") as HTMLDivElement;
    for(let i=0;i<dialogs.length;i++){
        dialogs[i].style.display = "none";
    }
    dialogBackground.style.display = "none";
}