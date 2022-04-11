import {newInstance} from "@jsplumb/browser-ui";
//import { Render } from "./render"
import {Render} from "./render";

export class Quest{
    constructor(data) {
       this.data = data;
    }

    static makeLoadRequest(url){
        return new Promise(function (resolve, reject) {
            let xmlhttp = new XMLHttpRequest();

            xmlhttp.onreadystatechange = () => {
                if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                    if (xmlhttp.status === 200) {
                        resolve(xmlhttp.responseText);
                    } else {
                        reject(xmlhttp.status);
                    }
                }
            };
            xmlhttp.open("GET", url, true);
            xmlhttp.send();
        });
    }

    static loadQuest(id){
        let url = '/api/db/quest/' + id.toString();

        return new Promise((resolve, reject) => {
            resolve(this.makeLoadRequest(url).then(data => {
                console.log("success");
                return new Quest(JSON.parse(data));
            }));
        });
    }

    static updateAnswer(id, answer){
        let url = 'api/answer/' + id;
        return new Promise((resolve, reject) => {
            let xmlhttp = new XMLHttpRequest();
            xmlhttp.open("PUT", url, true);

            xmlhttp.onreadystatechange = () => {
                if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                    if (xmlhttp.status === 200) {
                        console.log("resolve");
                        resolve(xmlhttp.responseText);
                    } else {
                        reject(xmlhttp.status);
                    }
                }
            };
            console.log(answer);
            xmlhttp.send(answer);
        });
    }

    static updateQuestion(id, question){
        let url = 'api/question/' + id;
        return new Promise((resolve, reject) => {
            let xmlhttp = new XMLHttpRequest();
            xmlhttp.open("PUT", url, true);

            xmlhttp.onreadystatechange = () => {
                if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                    if (xmlhttp.status === 200) {
                        console.log("resolve");
                        resolve(xmlhttp.responseText);
                    } else {
                        reject(xmlhttp.status);
                    }
                }
            };
            console.log(question);
            xmlhttp.send(question);
        });
    }

    save(){
        let url = 'api/save/' + this.data.quest_id;
        return new Promise((resolve, reject) => {
            let xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", url, true);

            xmlhttp.onreadystatechange = () => {
                if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                    if (xmlhttp.status === 200) {
                        console.log("resolve");
                        resolve(xmlhttp.responseText);
                    } else {
                        reject(xmlhttp.status);
                    }
                }
            };
            xmlhttp.send();
        });
    }
}
